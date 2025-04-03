import click
from pathlib import Path
import pandas as pd
from tira.check_format import JsonlFormat, _fmt
from tira.evaluators import WowsEvalEvaluator
from tira.rest_api_client import Client
from tira.third_party_integrations import upload_run_anonymous
from tirex_tracker import tracking
import json
from shutil import copytree, copyfile
import yaml

__version__ = "0.0.4"

import gzip

import tempfile

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
    dataset_id = None

    def evaluator():
        return WowsEvalEvaluator('*.jsonl', None, '*.jsonl', None, ['wows_tau_ap', 'wows_kendall', 'wows_spearman', 'wows_pearson'])

    if isinstance(truths, str):
        tira = Client()
        dataset_id = truths
        truths = tira.pd.truths(truths)
        if 'qrel_unknown_doc' not in truths.columns:
            truths = None
        else:
            truths = evaluator().normalize_data(truths)

    if not system_name:
        system_name = 'no-system-name'

    if not system_description:
        system_description = 'no-system-description'

    if tracking_results is not None and isinstance(tracking_results, dict):
        raise ValueError('I expected that the tracking_results is a TrackingHandle from tirex-tracker. Got:' + str(tracking_results))

    predictions = evaluator().normalize_data(predictions)
    if dataset_id is not None and upload:
        with tempfile.TemporaryDirectory() as f, tempfile.TemporaryDirectory() as meta:
            f = Path(f)
            meta = Path(meta)
            with gzip.open(f / 'predictions.jsonl.gz', 'wt') as output_file:
                for l in predictions:
                    output_file.write(json.dumps(l) + '\n')
            
            with tracking(system_name=system_name, system_description=system_description, export_file_path=meta / 'ir-metadata.yml') as tracking_results_code:
                    pass
            if tracking_results is None:
                tracking_results = tracking_results_code

            copytree(tracking_results_code._export_file_path.parent / ".tirex-tracker", f / ".tirex-tracker")
            metadata = ''
            with open(tracking_results._export_file_path, 'r') as tmp_f:
                for l in tmp_f:
                    if l.startswith('ir_metadata.end') or l.startswith('ir_metadata.start'):
                        continue
                    metadata += l

            with open(f / 'ir-metadata.yml', 'w') as tmp_f:
                tmp_f.write(metadata)

            upload_run_anonymous(f, dataset_id=dataset_id)
            #upload_run_anonymous(f, dataset_id='task_1/foo-pointwise-20250130_0-training', tira_client=Client(base_url='https://127.0.0.1:8080/', verify=False))

    if truths:
        ret = evaluator()._eval(predictions, truths)
        ret = {'system': system_name, 'tau_ap': ret['wows_tau_ap'], 'kendall': ret['wows_kendall'], 'spearman': ret['wows_spearman'], 'pearson': ret['wows_pearson']}
    else:
        print("No truth data is available yet. The evaluation is possible after the deadline when the truth data was published.")
        return None

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
