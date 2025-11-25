#!/usr/bin/env python3
from trectools import TrecQrel, TrecRun, TrecEval
from pathlib import Path
import pandas as pd
import json
from random import shuffle

def load_qrels(file_name):
    ret = TrecQrel()
    df = []
    with open(file_name, 'r') as f:
        for l in f:
            l = json.loads(l)
            df.append({"query": l["query_id"], "q0": "0", "docid": l["unknown_doc_id"], "rel": l["qrel_unknown_doc"]})

    ret.qrel_data = pd.DataFrame(df)
    return ret

def trec_run(query, docs):
    ret = TrecRun()
    df = []
    for doc in docs:
        df.append({"query": query, "q0": "0", "docid": doc, "rank": 1+len(df), "score": 1000-len(df), "system": "system"})
    ret.run_data = pd.DataFrame(df)
    return ret

def produce_rankings(qrels):
    query = list(qrels["query"].unique())[0]
    ret = []
    q = TrecQrel()
    q.qrels_data = qrels
    docs = list(qrels.sort_values("rel", ascending=False)["docid"])
    for i in range(0, 500):
        shuffle(docs)
        ret.append(trec_run(query, docs))

    ret_parsed = []
    ret = [trec_run(query, qrels.sort_values("rel", ascending=False)["docid"])] + \
        ret + \
        [trec_run(query, qrels.sort_values("rel", ascending=True)["docid"])]
    for run in ret:
        te = TrecEval(run, q)
        ret_parsed.append({"run": run, "ndcg": te.get_ndcg(depth=10)})
    return ret_parsed

def process(directory):
    qrels = load_qrels(directory / "labels.jsonl")
    final_runs = [[] for i in range(20)]
    
    for query in qrels.qrel_data["query"].unique():
        out_dir = directory/ "synthetic-runs"/ query
        out_dir.mkdir(exist_ok=True, parents=True)
        qrels_for_query = qrels.qrel_data[qrels.qrel_data["query"] == query].copy()
        runs = produce_rankings(qrels_for_query)
        selected_runs = []
        lower_bound = 0.99
        while lower_bound >= 0:
            upper_bound = lower_bound + 0.02
            for run in runs:
                if run["ndcg"] >= lower_bound and run["ndcg"] <= upper_bound:
                    selected_runs.append(run)
                    break

            lower_bound -= 0.02

        q = TrecQrel()
        q.qrels_data = qrels_for_query
        scores = []
        num = 0
        for run in selected_runs:
            te = TrecEval(run["run"], q)
            scores.append(te.get_ndcg(depth=10))
            run["run"].run_data.to_csv(out_dir / f"{num}.run.gz", sep=" ", header=False, index=False)
            num += 1
            Path(query)
        print("\t", len(scores), ":", scores)
            
        print("\n\n\n")

if __name__ == '__main__':
    process(Path('data'))

