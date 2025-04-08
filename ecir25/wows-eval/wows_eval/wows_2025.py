#!/usr/bin/env python3
from tira.rest_api_client import Client
from wows_eval.correlation import WowsCorrelationEvalEvaluator
from pathlib import Path
tira = Client()
import pandas as pd

TASK_ID = 'wows-eval'
DATASETS = ["pointwise-20250309-test", "pairwise-20250309-test"]
DATA_DIR = Path("/home/maik/workspace/wows-code/ecir25/wows-eval/build-runs/data")

def evaluator():
    ret = WowsCorrelationEvalEvaluator('*.jsonl', None, '*.jsonl', None, ['wows_tau_ap', 'wows_kendall', 'wows_spearman', 'wows_pearson'])
    ret.throw_if_conf_invalid({"run_dirs": [DATA_DIR / "synthetic-runs"]})
    return ret


df = []

for dataset in DATASETS:
    submissions = tira.submissions(TASK_ID, dataset)
    for _, i in submissions.iterrows():
        i = i.to_dict()
        if 'evaluator' in i['software'] or 'naive' in i['software']:
            continue
        print(i['team'], i['software'])
        ev = {"dataset": dataset, "team": i['team'], "approach": i['software']}

        run_dir = tira.get_run_output(f"{TASK_ID}/{i['team']}/{i['software']}", dataset)

        df.append(evaluator().evaluate(Path(run_dir), DATA_DIR / "truths" / dataset))

pd.DataFrame(df).to_json("evaluation.jsonl", lines=True, orient="records")