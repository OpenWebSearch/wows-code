---
configs:
- config_name: inputs
  data_files:
  - split: test
    path: ["corpus.jsonl.gz", "queries.jsonl"]
- config_name: truths
  data_files:
  - split: test
    path: ["qrels.txt", "queries.jsonl", "dataset-metadata.json", "config.json", "subsample.json"]

tira_configs:
  resolve_inputs_to: "."
  resolve_truths_to: "."
  baseline:
    link: https://github.com/reneuir/lsr-benchmark/tree/main/step-03-retrieval-approaches/lexical/pyterrier-pisa
    command: /run-pyterrier-pisa.py --dataset $inputDataset --output $outputDir
    format:
      name: ["run-with-metadata", "lightning-ir-document-embeddings", "lightning-ir-query-embeddings"]
  input_format:
    name: "lsr-benchmark-inputs"
    config:
      max_size_mb: 700
  truth_format:
    name: "qrels.txt"
  evaluator:
    measures: ["nDCG@10","P@10"]
---

# The Test Dataset created in the Jena and Kassel IR courses


