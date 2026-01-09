# OWS-Curlie-2025 - The Open Web Search Curlie 2025 test collection

This repository contains the Open Web Search Curlie 2025 test collection ([collection home page](https://dashboard.ows.eu/corpora/b510baa6-ebd2-11f0-8c43-02a47ca5d9fd)). The collection was created by taking six months worth of crawl data (March 1st until August 31st, 2025) from the Open Web Search project and transforming it using the standard Open Web Search preprocessing and indexing pipelines. We have only included data from the `curlie` subcollection (webpages that have an associated label in [the Curlie directory](https://curlie.org/)), and filtered on English documents.

## Contents

The collection contains three data splits: `radboud`, `radboud-val` and `jena-kassel`. For each split, students from the universities of Radboud, Jena and Kassel have provided topics and relevance assessments. The `radboud-val` split is a validation dataset that contains qrels; the other two splits are test collections and qrels are withheld. We have [subsampled](https://downloads.webis.de/publications/papers/froebe_2025c.pdf) the corpus for each split to keep the size of the collection manageable.

Each split contains the following files:
- `topics.tsv`: the topics for the split
- `subsample.parquet`: the subsampled collection, created by running a number of (cheap) retrieval models for the topic set and only retaining those documents that were retrieved at least once. The Parquet files contain the standard [Open Web Search preprocessing metadata](https://opencode.it4i.eu/openwebsearcheu-public/preprocessing-pipeline/#schema).
- `subsample.jsonl.gz`: the same subsampled collection, but in a simplified JSON format.
- `subsample_embeddings.parquet`: Jina V3 embeddings derived in the Open Web Search GPU processing pipeline
- _(For the validation split only)_ `qrels.txt`: the qrels for the validation set

The collection may be updated with more files, like pre-computed CIFF indexes for sparse retrieval or anchor text data. We will also release the full collection alongside the subsampled versions.

## Usage

To use the dataset, you first have to download the data using `owilix`, our command line tool for access to the Open Web Index. Then, you can either process the data yourself, use our custom `ir-datasets-owi` Python package to obtain an easy-to-use `ir-datasets` wrapper around the dataset.

### Downloading the data with Owilix

First, download [owilix](https://opencode.it4i.eu/openwebsearcheu-public/owi-cli). Our recommended installation approach is to use the one-line install script:

    https://opencode.it4i.eu/openwebsearcheu-public/owi-cli

You then get access to an `owilix` command line application. Please refer to [the owilix documentation](https://openwebsearcheu-public.pages.it4i.eu/owi-cli/) for more information on how to use it. For now, issue the following command to list the dataset and its contents (be sure to accept the license agreement when it pops up):

    owilix remote ls 'all/title=Open Web Search Curlie 2025' --file-details --files '*'

You can download the data to your local machine by using `owilix pull`:

    owilix remote pull 'all/title=Open Web Search Curlie 2025'

Note that you can select only certain files (e.g. if you do not need the JSON version of the subsampled corpus, or are only interested in a certain split) by using the `files` option:

    owilix remote pull 'all/title=Open Web Search Curlie 2025' 'files=**/*.parquet'

The files will be downloaded to the following directory (with the default `owilix` configuration):

    ~/.owi/public/special/b510baa6-ebd2-11f0-8c43-02a47ca5d9fd

### Loading the collection with ir-datasets

We have created a custom `ir-datasets` integration for the OWS-Curlie-2025 collection ([source code](https://github.com/OpenWebSearch/wows-code/tree/main/ecir26/corpus-construction/ir-datasets-owi)). To download the integration, simply issue:

    pip install ir-datasets-owi

Then, make sure that the collection can be found in your `ir-datasets` home directory:

    ln -s ~/.owi/public/special/b510baa6-ebd2-11f0-8c43-02a47ca5d9fd ~/.ir_datasets/ows-curlie-2025

You can now use the `ir-datasets` integration as follows:

```python
import ir_datasets_owi
import ir_datasets

ir_datasets_owi.register()

dataset = ir_datasets.load("ows-curlie-2025/radboud-val")

for doc in dataset.docs_iter():
    print(doc)
```

The documents have the following fields:
- `doc_id`: the document identifier (a SHA-256 hash of the normalized URL)
- `url`: the page URL
- `main_content`: the body of the web page with [minimal HTML structure](https://resiliparse.chatnoir.eu/en/stable/man/extract/html2text.html#minimal-html-conversion)
- `title`: the title of the web page
- `description`: the meta description of the web page
- `plain_text`: the `main_content` field with all HTML removed
- `default_text()`: a concatenation of `title` and `plain_text`

We also provide a short-hand version that combines `ir_datasets_owi.register` and `ir_datasets.load`:

```python
import ir_datasets_owi

dataset = ir_datasets_owi.load("ows-curlie-2025/radboud-val")
```

Both the `register` and the `load` methods support an optional `batch_size` parameter, which indicates how many documents are materialized per batch (higher is faster, but consumes more memory). The default of 2048 should be sufficient for most cases.

## Submitting runs

We accept either Docker submissions or run file submissions to [Tira/TIREx](https://tira.io). More information on submissions will follow soon.
