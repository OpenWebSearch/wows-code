# ChatNoir Baseline

This is a [chatnoir-pyterrier](https://github.com/chatnoir-eu/chatnoir-pyterrier) baseline. This baseline submits builds runs via submitting the title respectively the description against [ChatNoir](https://www.chatnoir.eu/) using BM25 respectively the default ChatNoir retrieval model (which is a form of weighted BM25f optimized for retrieval on the [ClueWebs](https://ir-datasets.com/clueweb09.html)).

## Overview

Get an overview of all possibilities to execute this baseline via:

```
./run-chatnoir.py --help
```

This should yield an output like:

```
Usage: run-chatnoir.py [OPTIONS]

Options:
  --k INTEGER                     The retrieval depth.
  --dataset [radboud-validation-20251114-training]
                                  The dataset.  [required]
  --output PATH                   The output directory.
  --query-field [title|description]
                                  The query field.
  --retrieval [bm25|default]      The retrieval model to use.
  --help                          Show this message and exit.
```

## Run All Variants

We run retreival via:

```
./run-chatnoir.py --dataset DATASET-ID --k 100 --query-field title --retrieval bm25
./run-chatnoir.py --dataset DATASET-ID --k 100 --query-field description --retrieval bm25
./run-chatnoir.py --dataset DATASET-ID --k 10 --query-field title --retrieval default
./run-chatnoir.py --dataset DATASET-ID --k 10 --query-field description --retrieval default
```
