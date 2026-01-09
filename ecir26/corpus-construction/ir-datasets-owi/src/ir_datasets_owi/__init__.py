import contextlib
from pathlib import Path
from typing import NamedTuple
import duckdb

import ir_datasets
from ir_datasets.datasets.base import Dataset
from ir_datasets.formats.base import BaseDocs, GenericDoc
from ir_datasets.formats.tsv import TsvQueries
from ir_datasets.formats.trec import TrecQrels
from ir_datasets.indices.base import Docstore


DATASET_ID = "ows-curlie-2025"

SPLITS = ["radboud-val", "radboud", "jena-kassel"]

QRELS_DEFS = {
    3: "perfectly_relevant",
    2: "highly_relevant",
    1: "related",
    0: "irrelevant",
    -2: "spam",
}


class OWIDoc(NamedTuple):
    doc_id: str
    url: str
    main_content: str
    title: str
    description: str

    @property
    def plain_text(self) -> str:
        return ir_datasets.util.sax_html_parser(self.main_content, fields=[None])[0]

    def default_text(self):
        result = []
        if self.title:
            result.append(self.title)
        if self.main_content:
            result.append(self.plain_text)

        return " ".join(result)


class ExtractedPath:
    def __init__(self, path: Path):
        self._path = path

    def path(self, force=True):
        if force and not self._path.exists():
            raise FileNotFoundError(self._path)
        return self._path

    @contextlib.contextmanager
    def stream(self):
        with open(self._path, "rb") as f:
            yield f


class ParquetDocs(BaseDocs):
    def __init__(self, path, doc_cls=GenericDoc, batch_size: int = 2048):
        super().__init__()
        self._path = path
        self._doc_cls = doc_cls
        self._batch_size = batch_size

    def docs_path(self, force=True):
        return self._path

    def docs_iter(self):
        fields = ", ".join(self._doc_cls._fields)
        results = duckdb.query(f"SELECT {fields} FROM (SELECT * RENAME (id AS doc_id) FROM read_parquet('{self._path}'));")

        while batch := results.fetchmany(self._batch_size):
            for row in batch:
                yield self._doc_cls(*row)

    def docs_cls(self):
        return self._doc_cls

    def docs_count(self):
        return duckdb.query(f"SELECT COUNT(*) FROM read_parquet('{self._path}');").fetchone()[0]

    def docs_store(self):
        return ParquetDocstore(self._path, self._doc_cls)


class ParquetDocstore(Docstore):
    def __init__(self, path, doc_cls, id_field="doc_id", batch_size: int = 2048):
        super().__init__(doc_cls, id_field)
        self._path = path
        self._batch_size = batch_size

    def get_many_iter(self, doc_ids):
        fields = ", ".join(self._doc_cls._fields)
        doc_ids = ", ".join(f"'{doc_id}'" for doc_id in doc_ids)
        results = duckdb.query(f"SELECT {fields} FROM (SELECT * RENAME (id AS {self._id_field}) FROM read_parquet('{self._path}') WHERE {self._id_field} IN ({doc_ids}));")

        while batch := results.fetchmany(self._batch_size):
            for row in batch:
                yield self._doc_cls(*row)


def register(batch_size: int = 2048):
    base_path = ir_datasets.util.home_path() / DATASET_ID

    if not base_path.exists():
        raise NotADirectoryError(f"Expected {DATASET_ID} directory in ir-datasets home: {ir_datasets.util.home_path()}")

    def register_split(split_name: str, include_qrels: bool = False) -> Dataset:
        split_id = f"{DATASET_ID}/{split_name}"

        # Don't register datasets multiple times
        if split_id in ir_datasets.registry._registered:
            return

        docs = ParquetDocs(base_path / split_name / "subsample.parquet", doc_cls=OWIDoc, batch_size=batch_size)
        topics = TsvQueries(ExtractedPath(base_path / "topics.tsv"))

        if include_qrels:
            qrels = TrecQrels(ExtractedPath(base_path / "qrels.txt"), QRELS_DEFS)
            dataset = Dataset(docs, topics, qrels)
        else:
            dataset = Dataset(docs, topics)

        ir_datasets.registry.register(split_id, dataset)

    register_split("radboud-val", include_qrels=True)
    register_split("radboud")
    register_split("jena-kassel")


def load(dataset_id: str, batch_size: int = 2048):
    register(batch_size)
    return ir_datasets.load(dataset_id)
