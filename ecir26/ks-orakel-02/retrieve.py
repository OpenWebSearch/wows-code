#!/usr/bin/env python3
import click
import pyterrier as pt
from pathlib import Path
from tirex_tracker import tracking, ExportFormat
from tira.third_party_integrations import ir_datasets, ensure_pyterrier_is_loaded
from tqdm import tqdm
import re
from pyterrier_t5 import MonoT5ReRanker


def clean_query(q):
    q = re.sub(r"[^\w\s]", " ", q)
    return q

def extract_text_of_document(doc, field):
    if field == "default_text":
        return doc.default_text()
    elif field == "title":
        return doc.title
    elif field == "description":
        return doc.description


def get_index(dataset, field, output_path):
    index_dir = output_path / "indexes" / f"{dataset}-on-{field}2"
    if not index_dir.is_dir():
        print("Build new index")
        docs = []
        dataset = ir_datasets.load(f"ir-lab-wise-2025/{dataset}")

        for doc in tqdm(dataset.docs_iter(), "Pre-Process Documents"):
            docs.append({"docno": doc.doc_id, "text": extract_text_of_document(doc, field)})

        with tracking(export_file_path=index_dir / "index-metadata.yml", export_format=ExportFormat.IR_METADATA):
            pt.IterDictIndexer(str(index_dir.absolute()), meta={'docno' : 100, 'text': 200000}, verbose=True).index(docs)

    return pt.IndexFactory.of(str(index_dir.absolute()))


def run_retrieval(output, index, dataset, text_field_to_retrieve):
    tag = f"pyterrier-bm25-with-monoT5-Reranking-on-{text_field_to_retrieve}"
    target_dir = output / "runs" / dataset / tag
    target_file = target_dir / "run.txt.gz"

    if target_file.exists():
        return

    topics = pt.datasets.get_dataset(f"irds:ir-lab-wise-2025/{dataset}").get_topics("title")
    topics["query"] = topics["query"].apply(clean_query)

    bm25_1st = pt.terrier.Retriever(index, wmodel="BM25", controls={"bm25.b" : 0.9, "bm25.k_1": 2, "bm25.k_3": 0.5})
    bm25 = pt.terrier.Retriever(index, wmodel="BM25")
    monoT5 = MonoT5ReRanker()

    res = bm25 % 40 >> pt.text.get_text(index, "text") >> monoT5

    description = f"This is a PyTerrier retriever using the retrieval model bm25 retrieving on the {text_field_to_retrieve} text representation of the documents. The top 40 results are reranked with the monoT5ReRanker."

    with tracking(export_file_path=target_dir / "retrieval-metadata.yml", export_format=ExportFormat.IR_METADATA, system_description=description, system_name=tag):
        run = res(topics)

    pt.io.write_results(run, target_file)

@click.command()
@click.option("--dataset", type=click.Choice(["radboud-validation-20251114-training", "spot-check-20251122-training"]), required=True, help="The dataset.")
@click.option("--output", type=Path, required=False, default=Path("output"), help="The output directory.")
@click.option("--text-field-to-retrieve", type=click.Choice(["default_text", "title", "description"]), required=False, default="default_text", help="The text field of the documents on which to retrieve.")
def main(dataset, text_field_to_retrieve, output):
    ensure_pyterrier_is_loaded(is_offline=False)

    index = get_index(dataset, text_field_to_retrieve, output)
    run_retrieval(output, index, dataset, text_field_to_retrieve)
    

if __name__ == '__main__':
    main()