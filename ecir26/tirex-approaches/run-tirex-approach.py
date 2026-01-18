#!/usr/bin/env python3
import click
from tira.rest_api_client import Client
from tira.ir_datasets_loader import get_as_re_rank_input
from pathlib import Path
from tira.third_party_integrations import temporary_directory
from tirex_tracker import tracking, ExportFormat
import shutil
from tira.check_format import log_message, check_format, _fmt
from tira.io_utils import patch_ir_metadata
from tirex_tracker import register_metadata


def load_re_rank_input(dataset_id, approach_to_re_rank, depth=1000):
    tira = Client()
    file_to_rerank = Path(tira.get_run_output(approach_to_re_rank, dataset_id)) / "run.txt.gz"

    register_metadata({"data": {"test collection": {"name": dataset_id}}})

    return get_as_re_rank_input(file_to_rerank, depth, dataset_id)


@click.command()
@click.option("--dataset", type=click.Choice(["ir-lab-wise-2025/radboud-validation-20251114-training", "ir-lab-wise-2025/spot-check-20251122-training"]), required=True, help="The dataset.")
@click.option("--output", type=Path, required=False, default=Path("output"), help="The output directory.")
@click.option("--re-ranks", type=str, required=False, default="ir-lab-wise-2025/ows/pyterrier-BM25-on-default", help="The system that is re-ranked.")
@click.option("--tira-approach", type=str, default="tira-ir-starter/DFIZ Re-Rank (tira-ir-starter-pyterrier)", required=False, help="The tira approach to run (e.g., BM25, PL2, DirichletLM).")
@click.option("--gpu", type=str, default=None, required=False, help="The GPU to use")
@click.option("--tag", required=True, type=str)
def main(dataset, tira_approach, re_ranks, output, gpu, tag):
    if output.is_dir():
        return

    re_rank_input = load_re_rank_input(dataset, re_ranks)

    tira = Client()
    team, system_name = tira_approach.split("/")
    details = tira.public_system_details(team, system_name)

    if "ir_re_ranker" not in details or not details["ir_re_ranker"]:
        raise ValueError(f"not a re-ranker: {details}")

    gpu_device_ids = None
    if gpu:
        gpu_device_ids = [gpu]

    tmp_dir = temporary_directory()
    
    with tracking(export_file_path=output / "re-rank-metadata.yml", export_format=ExportFormat.IR_METADATA, system_name=tag):
        tira.local_execution.run(
            image=details["public_image_name"],
            command=details["command"],
            input_dir=re_rank_input,
            output_dir=tmp_dir,
            allow_network=False,
            gpu_device_ids=gpu_device_ids,
        )

    result, msg = check_format(Path(tmp_dir), ["run.txt"], {})
    if result != _fmt.OK:
        print(msg)
        raise ValueError(msg)

    shutil.move(output / "re-rank-metadata.yml", tmp_dir)
    shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(tmp_dir, output)


if __name__ == '__main__':
    main()
