#!/usr/bin/env python3
import click
import pyterrier as pt
from pathlib import Path
from tira.third_party_integrations import ensure_pyterrier_is_loaded
from tirex_tracker import tracking, ExportFormat
from tira.rest_api_client import Client
import pandas as pd
import json
from tqdm import tqdm


@click.command()
@click.option("--dataset", type=click.Choice(["radboud-validation-20251114-training", "spot-check-20251122-training"]), required=True, help="The dataset.")
@click.option("--output", type=Path, required=True, help="The output directory.")
@click.option("--text-field", type=click.Choice(["default_text", "title", "description"]), required=False, default="title", help="The text field to index.")
def main(dataset, text_field, output):
    pt.Artifact.from_url(f"tira:{dataset}/ows/pyterrier-index-default")

    tag = f"pyterrier-{text_field}"
    description = f"This is a PyTerrier index that indexes the field {text_field} with default settings."
    corpus_file = Client().download_dataset(None, dataset) / "corpus.jsonl.gz"
    lines = pd.read_json(corpus_file, lines=True)

    docs = []
    for _, l in tqdm(lines.iterrows(), "load docs"):
        docs.append({"docno": l["doc_id"], "text": l[text_field]})

    with tracking(export_file_path=output / "index-metadata.yml", export_format=ExportFormat.IR_METADATA, system_description=description, system_name=tag):
        pt.IterDictIndexer(str(output.absolute()), meta={'docno' : 100}).index(docs)


if __name__ == '__main__':
    main()

