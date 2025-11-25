from tira.evaluators import WowsEvalEvaluator

from pathlib import Path
from typing import List
from trectools import TrecQrel, TrecRun, TrecEval
import pandas as pd
from glob import glob

from statistics import mean

class WowsCorrelationEvalEvaluator(WowsEvalEvaluator):
    def throw_if_conf_invalid(self, config: dict) -> None:
        if 'run_dirs' not in config:
            raise ValueError('I need a run_dirs configuration')
        self.run_dirs = config['run_dirs']

    def to_qrels(self, query_id, sorted_data):
        ret = TrecQrel()
        qrels_data = []
        for (qrel, docno) in sorted_data:
            qrels_data.append({"query": query_id, "q0": "0", "docid": docno, "rel": qrel})
        
        ret.qrels_data = pd.DataFrame(qrels_data)
        return ret


    def _eval(self, run_data: List[dict], truth_data: List[dict]) -> dict:
        id_to_query_doc = {}
        pairwise = False
        predictions = self.normalize_data(run_data)
        truths = self.normalize_data(truth_data)
        from trectools import misc

        for i in truths:
            id_to_query_doc[i["id"]] = {
                "query_id": i["query_id"],
                "doc_id": i["unknown_doc_id"],
                "qrel": int(i["qrel_unknown_doc"]),
            }
            if "relevant_doc_id" in i:
                pairwise = True
                id_to_query_doc[i["id"]]["relevant_doc_id"] = i["relevant_doc_id"]

        predictions = {i["id"]: i for i in predictions}

        if predictions.keys() != id_to_query_doc.keys():
            raise ValueError("fooo")

        if pairwise:
            truths_rankings, predictions_rankings = self._WowsEvalEvaluator__pairwise_rankings(id_to_query_doc, predictions)
        else:
            truths_rankings, predictions_rankings = self._WowsEvalEvaluator__pointwise_rankings(id_to_query_doc, predictions)

        tau_ap = []
        kendall = []
        spearman = []
        pearson = []

        for query_id in truths_rankings.keys():
            truth_ranking = self._WowsEvalEvaluator__sorted(truths_rankings[query_id])
            predicted_ranking = self._WowsEvalEvaluator__sorted(predictions_rankings[query_id])

            truth_qrels = self.to_qrels(query_id, truth_ranking)
            pred_qrels = self.to_qrels(query_id, predicted_ranking)

            truth_eval = []
            pred_eval = []
            for run_dir in self.run_dirs:
                for run_name in glob(f'{run_dir}/{query_id}/*.run.gz'):
                    run_path = Path(run_name)
                    run = TrecRun(run_path)

                    assert run_path.name not in [i['doc_id'] for i in truth_eval]
                    assert run_path.name not in [i['doc_id'] for i in pred_eval]
                    pred_eval.append({"doc_id": run_path.name, "score": TrecEval(run, pred_qrels).get_ndcg(depth=10)})
                    truth_eval.append({"doc_id": run_path.name, "score": TrecEval(run, truth_qrels).get_ndcg(depth=10)})

            assert len(pred_eval) > 10
            assert len(truth_eval) > 10
            pred_eval = self._WowsEvalEvaluator__sorted(pred_eval)
            truth_eval = self._WowsEvalEvaluator__sorted(truth_eval)
            tau_ap.append(misc.get_correlation(truth_eval, pred_eval, correlation="tauap")[0])
            kendall.append(misc.get_correlation(truth_eval, pred_eval, correlation="kendall")[0])
            spearman.append(misc.get_correlation(truth_eval, pred_eval, correlation="spearman")[0])
            pearson.append(misc.get_correlation(truth_eval, pred_eval, correlation="pearson")[0])

        ret = {
            "wows_tau_ap": mean(tau_ap),
            "wows_kendall": mean(kendall),
            "wows_spearman": mean(spearman),
            "wows_pearson": mean(pearson),
        }
        return {i: ret[i] for i in self._measures}