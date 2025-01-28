import click
from pathlib import Path
from trectools import misc
import pandas as pd
from tira.check_format import JsonlFormat, _fmt
from statistics import mean

__version__ = "0.0.1"

def __sorted(ret):
    ret = pd.DataFrame(ret)
    ret = ret.sort_values(["score","doc_id"], ascending=[False,True])

    return ret['doc_id']


def evaluate(predictions, truths):
    id_to_query_doc = {}
    truths_rankings = {}
    predictions_rankings = {}

    for i in truths:
        id_to_query_doc[i['id']] = {'query_id': i['query_id'], 'doc_id': i['unknown_doc_id'], 'qrel': i['qrel_unknown_doc']}

    predictions = {i['id']: i for i in predictions}

    if predictions.keys() != id_to_query_doc.keys():
        raise ValueError('fooo')

    for k, v in id_to_query_doc.items():
        if v['query_id'] not in truths_rankings:
            truths_rankings[v['query_id']] = []
            predictions_rankings[v['query_id']] = []

        truths_rankings[v['query_id']].append({'doc_id': v['doc_id'], 'score': v['qrel']})
        predictions_rankings[v['query_id']].append({'doc_id': v['doc_id'], 'score': predictions[k]['probability_relevant']})

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