import unittest

from wows_eval import evaluate
from tirex_tracker import tracking

class TestEvaluationTest(unittest.TestCase):
    def test_perfect_correlation_01(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = [
            {"id": "1", "probability_relevant": 2},
            {"id": "2", "probability_relevant": 2},
            {"id": "3", "probability_relevant": 3},
            {"id": "4", "probability_relevant": 3},
            {"id": "5", "probability_relevant": 1},
            {"id": "6", "probability_relevant": 1},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data, 'system_name', 'description', return_df=False)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_perfect_correlation_02(self):
        expected = {'tau_ap': 1.0, 'kendall': 1.0, 'pearson': 1.0, 'spearman': 1.0}

        predictions = [
            {"id": "1", "probability_relevant": 20},
            {"id": "2", "probability_relevant": 20},
            {"id": "3", "probability_relevant": 30},
            {"id": "4", "probability_relevant": 30},
            {"id": "5", "probability_relevant": 10},
            {"id": "6", "probability_relevant": 10},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data, 'system_name', 'description', return_df=False)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_non_perfect_correlation_01(self):
        expected = {'tau_ap': 0.5, 'kendall': 0.33333333333, 'pearson': 0.5, 'spearman': 0.5}

        predictions = [
            {"id": "1", "probability_relevant": 20},
            {"id": "2", "probability_relevant": 20},
            {"id": "3", "probability_relevant": 30},
            {"id": "4", "probability_relevant": 30},
            {"id": "5", "probability_relevant": 21},
            {"id": "6", "probability_relevant": 21},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data, 'system_name', 'description', return_df=False)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)


    def test_non_perfect_correlation_02(self):
        expected = {'tau_ap': 0.5, 'kendall': 0.33333333333, 'pearson': 0.5, 'spearman': 0.5}

        predictions = [
            {"id": "1", "probability_relevant": 1},
            {"id": "2", "probability_relevant": 1},
            {"id": "3", "probability_relevant": 3},
            {"id": "4", "probability_relevant": 3},
            {"id": "5", "probability_relevant": 2},
            {"id": "6", "probability_relevant": 2},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data, 'system_name', 'description', return_df=False)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_least_non_perfect_correlation_01(self):
        expected = {'tau_ap': -0.5, 'kendall': -0.33333333333, 'pearson': -0.5, 'spearman': -0.5}

        predictions = [
            {"id": "1", "probability_relevant": 1},
            {"id": "2", "probability_relevant": 1},
            {"id": "3", "probability_relevant": 2},
            {"id": "4", "probability_relevant": 2},
            {"id": "5", "probability_relevant": 3},
            {"id": "6", "probability_relevant": 3},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual = evaluate(predictions, truth_data, 'system_name', 'description', return_df=False)
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)

    def test_least_non_perfect_correlation_02(self):
        expected = {'tau_ap': -0.5, 'kendall': -0.33333333333, 'pearson': -0.5, 'spearman': -0.5}

        predictions = [
            {"id": "1", "probability_relevant": 1},
            {"id": "2", "probability_relevant": 1},
            {"id": "3", "probability_relevant": 2},
            {"id": "4", "probability_relevant": 2},
            {"id": "5", "probability_relevant": 3},
            {"id": "6", "probability_relevant": 3},
        ]
        truth_data = [
            {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
            {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
            {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
        ]

        actual_df = evaluate(predictions, truth_data, 'system_name', 'description')
        self.assertEqual(1, len(actual_df))
        actual = actual_df.iloc[0].to_dict()
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)


    def test_least_non_perfect_correlation_03(self):
        with tracking() as tracking_results:
            expected = {'tau_ap': -0.5, 'kendall': -0.33333333333, 'pearson': -0.5, 'spearman': -0.5}

            predictions = [
                {"id": "1", "probability_relevant": 1},
                {"id": "2", "probability_relevant": 1},
                {"id": "3", "probability_relevant": 2},
                {"id": "4", "probability_relevant": 2},
                {"id": "5", "probability_relevant": 3},
                {"id": "6", "probability_relevant": 3},
            ]
            truth_data = [
                {"id": "1", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
                {"id": "2", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-1", "qrel_unknown_doc": 2},
                {"id": "3", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
                {"id": "4", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-2", "qrel_unknown_doc": 3},
                {"id": "5", "query_id": "qid-1", "relevant_doc_id": "a", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
                {"id": "6", "query_id": "qid-1", "relevant_doc_id": "b", "unknown_doc_id": "d-3", "qrel_unknown_doc": 1},
            ]

        actual_df = evaluate(predictions, truth_data, 'system_name', 'description', tracking_results=tracking_results)
        self.assertEqual(1, len(actual_df))
        actual = actual_df.iloc[0].to_dict()
        for k in expected:
            self.assertAlmostEqual(expected[k], actual[k], delta=0.00001, msg=k)