import click
from pathlib import Path
from trectools import misc
import pandas as pd
from tira.check_format import JsonlFormat, _fmt
from tira.rest_api_client import Client
from tira.third_party_integrations import upload_run_anonymous
from statistics import mean
from tirex_tracker import tracked, TrackingHandle, Measure, ALL_MEASURES
import json
import yaml

__version__ = "0.0.2"

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

    for k, v in id_to_query_doc.items():
        if v['query_id'] not in truths_rankings:
            truths_rankings[v['query_id']] = {}
            predictions_rankings[v['query_id']] = {}

        if v['doc_id'] not in truths_rankings[v['query_id']]:
            truths_rankings[v['query_id']][v['doc_id']] = v['qrel']
        
        if v['doc_id'] not in predictions_rankings[v['query_id']]:
            predictions_rankings[v['query_id']][v['doc_id']] = 0

        predictions_rankings[v['query_id']][v['doc_id']] += float(predictions[k]['probability_relevant'])


    ret_truths_ranking = {}
    ret_predictions_rankings = {}

    for qid, docids in truths_rankings.items():
        ret_truths_ranking[qid] = [{'doc_id': i, 'score': truths_rankings[qid][i]} for i in docids]

    for qid, docids in predictions_rankings.items():
        ret_predictions_rankings[qid] = [{'doc_id': i, 'score': predictions_rankings[qid][i]} for i in docids]

    return ret_truths_ranking, ret_predictions_rankings


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


def evaluate(predictions, truths, system_name=None, system_description=None, upload=False, tracking_results=None, return_df=True):
    """Evaluate the predictions (a dataframe or a list of dictionaries) against the truths. We calculate ranking correlations between the predicted probabilities that documents are relevant against the ground truth ranking when ordering documents by their ground truth relevance labels.

    Args:
        predictions (a dataframe or a list of dictionaries): The predictions made by a relevance assessor. Each entry must contain a field "id" and a field "probability_relevant".
        truths (a dataset identifier for the tira dataset or a list of dictionaries or a dataframe): The ground truth relevance labels for each query--document pair.
        system_name (str, optional): The name of your system. Defaults to None.
        system_description (str, optional): The description of your system. Defaults to None.
        upload (bool, optional): Should your run be uploaded to TIRA. Defaults to False.
        tracking_results (TrackingHandle, optional): A tirex-tracker trace of your experiment execution. Defaults to None.
        return_df (bool, optional): return the evaluation results as DataFrame. Defaults to True.

    Raises:
        ValueError: Raised if there is an error.

    Returns:
        DataFrame/Dictionary: The correlation between the predicted probabilities that documents are relevant and the ground truth relevance labels.
    """
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

    if not system_name:
        system_name = 'no-system-name'

    if not system_description:
        system_description = 'no-system-description'

    if tracking_results is not None and isinstance(tracking_results, dict):
        raise ValueError('I expected that the tracking_results is a TrackingHandle from tirex-tracker. Got:' + str(tracking_results))

    if dataset_id is not None and upload:
        with tempfile.TemporaryDirectory() as f:
            f = Path(f)
            with gzip.open(f / 'predictions.jsonl.gz', 'wt') as output_file:
                for l in predictions.values():
                    output_file.write(json.dumps(l) + '\n')
            
            mesures_to_skip = set([
                Measure.TIME_ELAPSED_WALL_CLOCK_MS,
                Measure.TIME_ELAPSED_USER_MS,
                Measure.TIME_ELAPSED_SYSTEM_MS,
                Measure.CPU_USED_PROCESS_PERCENT,
                Measure.CPU_USED_SYSTEM_PERCENT,
                Measure.CPU_ENERGY_SYSTEM_JOULES,
                Measure.RAM_USED_PROCESS_KB,
                Measure.RAM_USED_SYSTEM_MB,
                Measure.RAM_AVAILABLE_SYSTEM_MB,
                Measure.RAM_ENERGY_SYSTEM_JOULES,
                Measure.GPU_USED_PROCESS_PERCENT,
                Measure.GPU_USED_SYSTEM_PERCENT,
                Measure.GPU_VRAM_USED_PROCESS_MB,
                Measure.GPU_VRAM_USED_SYSTEM_MB,
                Measure.GPU_ENERGY_SYSTEM_JOULES])
            measures = [i for i in ALL_MEASURES if i not in mesures_to_skip]

            if tracking_results is None:
                with tracked(f_or_measures=measures, system_name=system_name, system_description=system_description) as tracking_results:
                    pass

            with open(f / 'ir-metadata.yml', 'w') as yaml_file:
                yaml.dump(tracking_results, yaml_file)
            upload_run_anonymous(f, dataset_id=dataset_id)
            #upload_run_anonymous(f, dataset_id='task_1/foo-pointwise-20250130_0-training', tira_client=Client(base_url='https://127.0.0.1:8080/', verify=False))


    ret = {'system': system_name, 'tau_ap': mean(tau_ap), 'kendall': mean(kendall), 'spearman': mean(spearman), 'pearson': mean(pearson)}

    if return_df:
        return pd.DataFrame([ret])
    else:
        return ret


@click.command(help="Evaluate the predictions of your relevance assessor passed in a file PREDICTIONS against the TRUTHS (either a file or a string with the TIRA dataset ID). wows-eval calculates ranking correlations between the predicted probabilities that documents are relevant against the ground truth ranking when ordering documents by their ground truth relevance labels.")
@click.argument('predictions', type=str)
@click.argument('truths', type=str)
@click.option('--upload', type=bool, is_flag=True, help="Upload predictions to TIRA.")
def cli(predictions: str, truths: str, upload: bool):
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
    elif isinstance(truths, str):
        actual_truths = truths
    else:
        print('Could not load the truths:\n\n' + msg)
        return

    print(evaluate(actual_predictions, actual_truths, return_df=False, upload=upload))


if __name__ == '__main__':
    cli()
