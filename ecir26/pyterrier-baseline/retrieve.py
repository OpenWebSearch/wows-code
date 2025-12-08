#!/usr/bin/env python3
import click
import pyterrier as pt
from pathlib import Path
from tira.third_party_integrations import ensure_pyterrier_is_loaded
from tirex_tracker import tracking, ExportFormat


@click.command()
@click.option("--dataset", type=click.Choice(["radboud-validation-20251114-training", "spot-check-20251122-training"]), required=True, help="The dataset.")
@click.option("--output", type=Path, required=True, help="The output directory.")
@click.option("--retrieval-model", type=str, default="BM25", required=False, help="The retrieval model.")
@click.option("--index", type=click.Choice(["default", "title", "description"]), required=False, default="default", help="The text field of the index on which to retrieve.")
def main(dataset, index, retrieval_model, output):
    ensure_pyterrier_is_loaded()
    pt_index = pt.Artifact.from_url(f"tira:{dataset}/ows/pyterrier-index-{index}")
    topics = pt.datasets.get_dataset(f"irds:ir-lab-wise-2025/{dataset}").get_topics("title")
    retriever = pt.terrier.Retriever(pt_index, wmodel=retrieval_model)

    tag = f"pyterrier-{retrieval_model}-on-{index}"
    target_dir = output / dataset / tag
    description = f"This is a PyTerrier retriever using the retrieval model {retriever} retrieving on the {index} text representation of the documents. Everything is set to the defaults."

    with tracking(export_file_path=target_dir / "ir-metadata.yml", export_format=ExportFormat.IR_METADATA, system_description=description, system_name=tag):
        run = retriever(topics)

    pt.io.write_results(run, target_dir / "run.txt.gz")

if __name__ == '__main__':
    main()

