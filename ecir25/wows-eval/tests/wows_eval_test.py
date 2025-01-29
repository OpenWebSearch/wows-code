import unittest

from wows_eval import evaluate
import pandas as pd

class TestEvaluationTest(unittest.TestCase):
    def test_perfect_correlation_01(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = [
            {"id": "1", "probability_relevant": 2},
            {"id": "2", "probability_relevant": 1},
            {"id": "3", "probability_relevant": 3},
            {"id": "4", "probability_relevant": 1},
            {"id": "5", "probability_relevant": 1},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_perfect_correlation_01_for_df(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = pd.DataFrame([
            {"id": "1", "probability_relevant": 2},
            {"id": "2", "probability_relevant": 1},
            {"id": "3", "probability_relevant": 3},
            {"id": "4", "probability_relevant": 1},
            {"id": "5", "probability_relevant": 1},
        ])
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},

        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_perfect_correlation_02(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = [
            {"id": "1", "probability_relevant": 0.2},
            {"id": "2", "probability_relevant": 0.1},
            {"id": "3", "probability_relevant": 0.3},
            {"id": "4", "probability_relevant": 0.1},
            {"id": "5", "probability_relevant": 0.1},

        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},

        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_perfect_correlation_03(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = [
            {"id": "1", "probability_relevant": 10.2},
            {"id": "2", "probability_relevant": 10.1},
            {"id": "3", "probability_relevant": 10.3},
            {"id": "4", "probability_relevant": 10.1},
            {"id": "5", "probability_relevant": 10.1},

        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},

        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_perfect_inverse_correlation_01(self):
        expected = {'tau_ap': 0.0, 'kendall': -0.39999999, 'pearson': -0.6, 'spearman': -0.6}

        predictions = [
            {"id": "1", "probability_relevant": -2},
            {"id": "2", "probability_relevant": -1},
            {"id": "3", "probability_relevant": -3},
            {"id": "4", "probability_relevant": -1},
            {"id": "5", "probability_relevant": -1},

        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},

        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)


    def test_perfect_inverse_correlation_02(self):
        expected = {'tau_ap': 0.0, 'kendall': -0.39999999, 'pearson': -0.6, 'spearman': -0.6}

        predictions = [
            {"id": "1", "probability_relevant": -0.2},
            {"id": "2", "probability_relevant": -0.1},
            {"id": "3", "probability_relevant": -0.3},
            {"id": "4", "probability_relevant": -0.1},
            {"id": "5", "probability_relevant": -0.1},

        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "unknown_doc_id": "d-2", "qrel_unknown_doc": 1},
            {"id": "3", "query_id": "qid-1", "unknown_doc_id": "d-3", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "unknown_doc_id": "d-4", "qrel_unknown_doc": 1},
            {"id": "5", "query_id": "qid-1", "unknown_doc_id": "d-5", "qrel_unknown_doc": 1},

        ]

        actual = evaluate(predictions, truth_data)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)