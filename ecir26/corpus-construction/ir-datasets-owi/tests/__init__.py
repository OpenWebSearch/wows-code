import unittest

import ir_datasets
import ir_datasets_owi


class TestCollection(unittest.TestCase):
    def setUp(self):
        ir_datasets_owi.register(batch_size=1)

        self.datasets = {
            split: ir_datasets.load(f"{ir_datasets_owi.DATASET_ID}/{split}")
            for split in ir_datasets_owi.SPLITS
        }

    def test_counts(self):
        counts = {
            "radboud-val": 63639,
            "radboud": 90852,
            "jena-kassel": 77382,
        }

        for split, count in counts.items():
            self.assertEqual(self.datasets[split].docs_count(), count)

    def test_docs_iter(self):
        first_ids = {
            "radboud-val": "000009267aaf52007d3e3095ed49b89503f5f23cfd7fb924f81c10a136953d7a",
            "radboud": "000021a7fc38c1f03aae6f7ec752065d8647e3085ad17e2e9b9ab1d372f3bef8",
            "jena-kassel": "000009267aaf52007d3e3095ed49b89503f5f23cfd7fb924f81c10a136953d7a"
        }

        for split, first_id in first_ids.items():
            first_doc = next(iter(self.datasets[split].docs_iter()))

            self.assertIsInstance(first_doc, ir_datasets_owi.OWIDoc)
            self.assertEqual(first_doc.doc_id, first_id)

    def test_docs_store(self):
        target_id = "ca07da4d2b00214a2bdeb33e2675d2b3b16a6ed4e06e54dfb03adf1137822b14"

        for split in ir_datasets_owi.SPLITS:
            doc = self.datasets[split].docs_store().get(target_id)

            self.assertIsInstance(doc, ir_datasets_owi.OWIDoc)
            self.assertEqual(doc.doc_id, target_id)

    def test_topics(self):
        first_ids = {
            "radboud-val": "3",
            "radboud": "1",
            "jena-kassel": "51"
        }

        for split, first_id in first_ids.items():
            first_query = next(iter(self.datasets[split].queries_iter()))

            self.assertIsInstance(first_query, ir_datasets.formats.base.GenericQuery)
            self.assertEqual(first_query.query_id, first_id)

if __name__ == '__main__':
    unittest.main()
