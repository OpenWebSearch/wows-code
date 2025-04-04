#!/usr/bin/env python3
from trectools import TrecQrel, TrecRun, TrecEval
from pathlib import Path
import pandas as pd
import json
from random import shuffle
import os

def load_qrels(file_name):
    ret = TrecQrel()
    df = []
    with open(file_name, 'r') as f:
        for l in f:
            l = json.loads(l)
            df.append({"query": l["query_id"], "q0": "0", "docid": l["unknown_doc_id"], "rel": l["qrel_unknown_doc"]})

    ret.qrel_data = pd.DataFrame(df)
    return ret

def trec_runs(directory, query):
    ret = []
    for f in os.listdir(directory / query):
        ret.append(TrecRun(directory / query / f))
    return ret

def process(directory, run_dir):
    qrels = load_qrels(directory / "labels.jsonl")
    final_runs = [[] for i in range(20)]
    
    for query in qrels.qrel_data["query"].unique():
        qrels_for_query = qrels.qrel_data[qrels.qrel_data["query"] == query].copy()
        runs = trec_runs(run_dir, query)

        q = TrecQrel()
        q.qrels_data = qrels_for_query
        scores = []
        for run in runs:
            te = TrecEval(run, q)
            scores.append(te.get_ndcg(depth=10))
        print("\t", len(scores), ":", scores)

if __name__ == '__main__':
    process(Path('data'), Path('data') / 'synthetic-runs')

