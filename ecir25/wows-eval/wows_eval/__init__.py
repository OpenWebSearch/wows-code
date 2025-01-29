import click
from pathlib import Path
from trectools import misc
import pandas as pd
from tira.check_format import JsonlFormat, _fmt
from tira.rest_api_client import Client
from tira.third_party_integrations import upload_run_anonymous
from statistics import mean
import json
from auto_ir_metadata import persist_ir_metadata

__version__ = "0.0.1"

import gzip

import tempfile


def __sorted(ret):
    ret = pd.DataFrame(ret)
    ret = ret.sort_values(["score","doc_id"], ascending=[False,True])
    return [(i['score'], i['doc_id']) for _, i in ret.iterrows()]


def __pointwise_rankings(id_to_query_doc, predictions):
    truths_rankings = {}
    predictions_rankings = {}

    for k, v in id_to_query_doc.items():
        if v['query_id'] not in truths_rankings:
            truths_rankings[v['query_id']] = []
            predictions_rankings[v['query_id']] = []

        truths_rankings[v['query_id']].append({'doc_id': v['doc_id'], 'score': v['qrel']})
        predictions_rankings[v['query_id']].append({'doc_id': v['doc_id'], 'score': float(predictions[k]['probability_relevant'])})

    return truths_rankings, predictions_rankings


def __pairwise_rankings(id_to_query_doc, predictions):
    truths_rankings = {}
    predictions_rankings = {}
    raise ValueError('Not yet implemented')


def __normalize_data(df):
    if isinstance(df, pd.DataFrame):
        return __normalize_data([i.to_dict() for _, i in df.iterrows()])
    else:
        ret = []
        for i in df.copy():
            i = i.copy()
            for field_to_delete in ['unknown']:
                if field_to_delete in i:
                    del i[field_to_delete]
            ret.append(i)
        return ret


def evaluate(predictions, truths):
    id_to_query_doc = {}
    pairwise = False
    predictions = __normalize_data(predictions)
    dataset_id = None
    if isinstance(truths, str):
        tira = Client()
        dataset_id = truths
        truths = tira.pd.truths(truths)
        truths = __normalize_data(truths)

    for i in truths:
        id_to_query_doc[i['id']] = {'query_id': i['query_id'], 'doc_id': i['unknown_doc_id'], 'qrel': int(i['qrel_unknown_doc'])}
        if 'relevant_doc_id' in i:
            pairwise = True
            id_to_query_doc[i['id']]['relevant_doc_id'] = i['relevant_doc_id']

    predictions = {i['id']: i for i in predictions}

    if predictions.keys() != id_to_query_doc.keys():
        raise ValueError('fooo')

    if pairwise:
        truths_rankings, predictions_rankings = __pairwise_rankings(id_to_query_doc, predictions)
    else:
        truths_rankings, predictions_rankings = __pointwise_rankings(id_to_query_doc, predictions)

    tau_ap = []
    kendall = []
    spearman = []
    pearson = []

    for query_id in truths_rankings.keys():
        truth_ranking = __sorted(truths_rankings[query_id])
        predicted_ranking = __sorted(predictions_rankings[query_id])

        tau_ap.append(misc.get_correlation(truth_ranking, predicted_ranking, correlation = "tauap")[0])
        kendall.append(misc.get_correlation(truth_ranking, predicted_ranking, correlation = "kendall")[0])
        spearman.append(misc.get_correlation(truth_ranking, predicted_ranking, correlation = "spearman")[0])
        pearson.append(misc.get_correlation(truth_ranking, predicted_ranking, correlation = "pearson")[0])

    if dataset_id is not None:
        with tempfile.TemporaryDirectory(delete=False) as f:
            f = Path(f)
            with gzip.open(f / 'predictions.jsonl.gz', 'wt') as output_file:
                for l in predictions.values():
                    output_file.write(json.dumps(l) + '\n')
            persist_ir_metadata(f)
            upload_run_anonymous(f, dataset_id=dataset_id)

    return {'tau_ap': mean(tau_ap), 'kendall': mean(kendall), 'spearman': mean(spearman), 'pearson': mean(pearson)}


@click.command()
@click.argument('predictions', type=str)
@click.argument('truths', type=str)
def cli(predictions: str, truths: str):
    predictions_formatter = JsonlFormat(('id', 'probability_relevant'))
    truths_formatter = JsonlFormat(('id', 'query_id', 'unknown_doc_id', 'qrel_unknown_doc'))

    result, msg = predictions_formatter.check_format(Path(predictions))

    if result != _fmt.OK:
        print('Could not load the predictions:\n\n' + msg)
        return 
    
    actual_predictions = predictions_formatter.all_lines(Path(predictions))
    actual_truths = None
    
    result, msg = truths_formatter.check_format(Path(truths))

    if result == _fmt.OK:
        actual_truths = truths_formatter.all_lines(Path(truths))
    else:
        print('Could not load the truths:\n\n' + msg)
        return

    print(evaluate(actual_predictions, actual_truths))


if __name__ == '__main__':
    cli()