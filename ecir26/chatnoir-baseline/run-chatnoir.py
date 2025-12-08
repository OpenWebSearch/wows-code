#!/usr/bin/env python3
import click
import pyterrier as pt
from pathlib import Path
from tira.third_party_integrations import ensure_pyterrier_is_loaded
from chatnoir_pyterrier import ChatNoirRetrieve
from tirex_tracker import tracking, ExportFormat


def load_topics(irds, field):
    ensure_pyterrier_is_loaded(patch_ir_datasets=True, is_offline=False)
    pt_dataset = pt.datasets.get_dataset(f"irds:ir-lab-wise-2025/{irds}")
    return pt_dataset.get_topics(field)


@click.command()
@click.option("--k", type=int, required=False, default=100, help="The retrieval depth.")
@click.option("--dataset", type=click.Choice(["radboud-validation-20251114-training"]), required=True, help="The dataset.")
@click.option("--output", type=Path, required=False, default=Path("runs"), help="The output directory.")
@click.option("--query-field", type=click.Choice(["title", "description"]), required=False, default="title", help="The query field.")
@click.option("--retrieval", type=click.Choice(["bm25", "default"]), required=False, default="bm25", help="The retrieval model to use.")
def main(dataset, query_field, output, retrieval, k):
    topics = load_topics(dataset, query_field)
    tag = f"chatnoir-{query_field}-{retrieval}-{k}"
    target_dir = output / dataset/ tag
    target_dir.mkdir(parents=True, exist_ok=True)
    description = f"This is a chatnoir-pyterrier baseline that retrieves the top-{k} results via the {query_field} field against ChatNoir using the {retrieval} model."

    with tracking(export_file_path=target_dir / "ir-metadata.yml", export_format=ExportFormat.IR_METADATA, system_description=description, system_name=tag):
        chatnoir = ChatNoirRetrieve(index="wows-owi/2025", search_method=retrieval, features=[], verbose=True, num_results=k, page_size=k)
        run = chatnoir(topics)

    pt.io.write_results(run, target_dir / "run.txt.gz")


if __name__ == '__main__':
    main()
