#!/usr/bin/env python3
import json
import click
from pathlib import Path
from tira.third_party_integrations import ir_datasets
from tqdm import tqdm
import gzip
import prompts
import re

from trectools import TrecPoolMaker, TrecRun, TrecQrel

def parse_llm_response(response: str) -> int:
    "This method is from UMBRELA https://github.com/castorini/umbrela/blob/main/src/umbrela/utils/common_utils.py and will be properly cited in the paper."
    response = response.strip().lower()
    valid_res = 1
    answer = ""
    patterns = [
        r'"o"\s*[:-=]?\s*(0|1|2|3)',
        r"\'o\'\s*[:-=]?\s*(0|1|2|3)",
        r"o\s*[:-=]?\s*(0|1|2|3)",
        r'"overall_score"\s*[:-=]?\s*(0|1|2|3)',
        r'"overall"\s*[:-=]?\s*(0|1|2|3)',
        r'"overall score"\s*[:-=]?\s*(0|1|2|3)',
        r'"final score"\s*[:-=]?\s*(0|1|2|3)',
        r'final score\s*[:-=]?\s*(0|1|2|3)',
        r"final score is (0|1|2|3)",
        r'"final_score"\s*[:-=]?\s*(0|1|2|3)',
        r'"score"\s*[:-=]?\s*(0|1|2|3)',
        r'"o_score"\s*[:-=]?\s*(0|1|2|3)',
        r"output score is (0|1|2|3)",
        r"score is (0|1|2|3)",
        r"[a-zA-Z]+\s+is\s+(0|1|2|3)\s",
        r"relevance category\s*[:-=]?\s*(0|1|2|3)",
        r"relevance category\s*[:-=]?\s*(0|1|2|3)",
        r"relevance category is (0|1|2|3)",
        r"it falls into the category (0|1|2|3)",
        r"category\s*(0|1|2|3)",
        r"relevance category (0|1|2|3)",
        r"relevance category for this passage would be (0|1|2|3)",
        r"the relevance category would be (0|1|2|3)",
        r"\n*(0|1|2|3)",
    ]
    for pattern in patterns:
        matched = None
        for m in re.finditer(pattern, response, re.IGNORECASE | re.MULTILINE | re.DOTALL):
            matched = m

        if matched:
            answer = matched.group(1).capitalize()
            break
    if answer == "":
        answer = "0"
        valid_res = 0
        print(f"Invalid response: {response}")
    return int(answer), valid_res


def pooling(directory, config):
    pooling_path = directory / config["runs"]
    pooling_depth = config["pooling_depth"]
    runs = []
    for run in tqdm(pooling_path.glob("*"), "pool runs"):
        runs += [TrecRun(run)]

    if len(runs) < 4:
        raise ValueError(f"not enough runs in {pooling_path}")
    
    return TrecPoolMaker().make_pool(runs, strategy='topX', topX=pooling_depth).pool

def read_all_predictons(directory):
    target_file = directory / "predictions.jsonl.gz"

    if not target_file.is_file():
        with gzip.open(target_file, "wt") as f:
            f.write("")

    with gzip.open(target_file, "rt") as f:
        ret = []
        for l in f:
            try:
                ret.append(json.loads(l))
            except:
                pass
        return ret

def predict(query, doc, config):
    prompt = config["prompt"]
    prompt_impl = getattr(prompts, prompt)

    assessor = LLMForRelevanceJudgment(prompt_impl, config["model"])
    predictions = []
    for segment in doc.segments[:3]:
        segment_text = segment["text"][:50000]
        predictions.append(assessor.generate(query.default_text(), segment_text))

    return json.dumps({"query_id": query.query_id, "doc_id": doc.doc_id, "predictions": predictions}) + '\n'

def process_query(directory, query, pool, ir_dataset, config):
    docs = set(pool[query.query_id])
    for qrel in ir_dataset.qrels_iter():
        if str(qrel.query_id) == str(query.query_id):
            docs.add(qrel.doc_id)

    predicted_docs = set()

    for i in read_all_predictons(directory):
        if str(i["query_id"]) == str(query.query_id):
            predicted_docs.add(i["doc_id"])

    docs_to_predict = [doc for doc in docs if doc not in predicted_docs]
    docs_store = ir_dataset.docs_store()

    skipped = 0
    with gzip.open(directory / "predictions.jsonl.gz", "at") as f:
        for doc in tqdm(docs_to_predict, "predict"):
            if doc not in docs_store:
                skipped += 1
                continue
            f.write(predict(query, docs_store.get(doc), config))
            f.flush()

    if skipped > 0:
        print(f"skipped {skipped} of {len(docs)} docs for query {query.query_id}")


class LLMForRelevanceJudgment():
    def __init__(self, prompt: str, model : str, preamble : str = None, **kwargs) -> None:
        """_summary_

        Args:
            prompt (_type_): _description_
            model (_type_): _description_
            preamble (_type_, optional): _description_. Defaults to None.
        """
        from openai import OpenAI as cli

        self._model = model # Model name
        self._client = cli(base_url="https://openrouter.ai/api/v1") # OpenAI client
        self._prompt = prompt # Outlines prompt
        self._preamble = preamble # System prompt
        self._kwargs = kwargs # All completion parameters e.g max_tokens, temperature ...

    def generate(self, query : str, passage : str):
        """ Generate a response with a instruct LLM.

        Args:
            query (str): the query
            passage (str): the document

        Returns:
            str: LLM response
        """
        messages = []
        if self._preamble:
            messages.append(
                {
                    "role": "system",
                    "content": self._preamble
                }
            )

        formatted = self._prompt(query, passage)
        messages.append({
            "role": "user",
            "content": formatted
        })

        output = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            **self._kwargs
        )
        try:
            return output.choices[0].message.to_dict()
        except:
            print("skip non-existing query")
            return None

@click.command()
@click.option('--directory', help='The directory with the configuration where all the outputs should be persisted in jsonl format.', type=Path, default=Path('data'))
def run_predictions(directory: Path):
    config = json.loads((directory / "config.json").read_text())

    pool = pooling(directory, config)

    ir_dataset = ir_datasets.load(config["tira-id"])
    for query in ir_dataset.queries_iter():
        process_query(directory, query, pool, ir_dataset, config)

    print("Write qrels")
    with open(directory / "qrels.txt", "w") as f:
        for pred in read_all_predictons(directory):
            score = max([0] + [parse_llm_response(p["content"] if p and "content" in p else "")[0] for p in pred["predictions"]])
            f.write(pred["query_id"] + " 0 " + pred["doc_id"] +  " "  + str(score) + "\n")
    print("Done :)")

if __name__ == '__main__':
    run_predictions()
