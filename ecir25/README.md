# Code and Tutorials for the [2nd International Workshop on Open Web Search](https://opensearchfoundation.org/en/events-osf/wows2025) #wows2025

This repository contains all code, tutorials, and baselines for the WOWS-EVAL shared task at [WOWS25](https://opensearchfoundation.org/en/events-osf/wows2025/)@[ECIR'25](https://ecir2025.eu/)

## Goal

## Data Format

We aim to collect pointwise and pairwise relevance assessors. An overview of all datasets for the shared task is available at [https://tira.io/datasets?query=wows-eval](https://archive.tira.io/datasets?query=wows-eval). Please use the smoke test datasets to ensure that your software works as expected before processing the larger test datasets.

### Pointwise Relevance Assessments

Given a query and a document, predict the probability that the document is relevant to the query. The data comes in jsonl format where each input line has the following fields:

- `id`: The identifier for the query-document pair.
- `query`: The query for which the relevance should be predicted.
- `unknown`: The text of the document for which the relevance to the `query` should be predicted.

You can directly load the dataset(s) into a [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) via the tira client (install via `pip3 install tira`) for simplified processing. For instance, execute the following command to load the pointwise smoke test dataset into a DataFrame (see [tira.io/datasets?query=wows-eval](https://archive.tira.io/datasets?query=wows-eval) for an complete overview of dataset identifiers):

```
from tira.rest_api_client import Client
tira = Client()
input_data = tira.pd.inputs('wows-eval/pointwise-smoke-test-20250128-training')
```

The dataset looks like this:

![example of pointwise data](figures/pointwise-data-example.png)

The task of an relevance assessor is to produce an output in jsonl with two fields per line:
- `id`: The identifier for the query-document pair.
- `probability_relevant`: The probability (between 0 for non-relevant and 1 for relevant) that the document is relevant to the query.

### Pairwise Relevance Assessments

Given a query, a known relevant document, and an document with an unknown relevance to a query, predict the probability that the unknown document is relevant to the query given the known relevant document.






## Step-by-Step Submission Guide

We use [TIRA](https://www.tira.io) aiming at run submissions enriched with [ir-metadata](https://www.ir-metadata.org/) to improve reproducibility.

### Step 1: Register to TIRA and to the WOWS-EVAL task

Please register at [tira.io](https://www.tira.io) and navigate to the [WOWS-EVAL](https://www.tira.io/task-overview/wows-eval/) task and click on "Register". You can choose your team name from a list of [fictional](https://en.wikipedia.org/wiki/Category:Fictional_librarians) and [real](https://en.wikipedia.org/wiki/List_of_librarians) librarians ([please drop a message](#contact) if your favourite team name is not in the list).

### Step 2: Install the wows-eval Script to Evaluate and Submit Your Solutions

We have created a python script `wows-eval` that you can use on the command line and in python to evaluate your relevance assessor.

### Step 3: Implement your Relevance Assessors

### Step 4: 


## Tutorials


## Resources

Important links/resources:
- [The workshop page](https://opensearchfoundation.org/en/events-osf/wows2025)
- [Software submissions](https://www.tira.io/task-overview/workshop-on-open-web-search/)
- [Baseline submissions](https://github.com/OpenWebSearch/wows-code/tree/main/ecir25/baselines)

# Contact

If you have any questions or problems, please do not hesitate to contact us via [the forum](https://www.tira.io/t/the-forum-for-the-2nd-international-workshop-on-open-web-search-wows2025) or via mail.

