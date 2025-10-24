#!/usr/bin/env python3
from typing import NamedTuple
import duckdb
import ir_datasets
from ir_datasets.formats.base import BaseDocs, GenericDoc
from ir_datasets.indices.base import Docstore
from ir_datasets.datasets.base import Dataset
from glob import glob
import gzip
import json
from tqdm import tqdm

con = duckdb.connect()
con.install_extension('httpfs')
con.load_extension('httpfs')
con.execute("""
        SET s3_access_key_id = '';
        SET s3_secret_access_key = '';
        SET s3_session_token = '';
        SET s3_endpoint = 'ir-teach-wise-2025.s3.data.webis.de';
        SET s3_url_style = 'virtual_hosted';
        SET s3_use_ssl = true;
    """)


class OWIDoc(NamedTuple):
    doc_id: str
    url: str
    main_content: str
    title: str
    description: str

    def default_text(self):
        return title + " " + self.main_content


class ParquetDocs(BaseDocs):
    def __init__(self, path, doc_cls=GenericDoc):
        super().__init__()
        self._path = path
        self._doc_cls = doc_cls

    def docs_path(self, force=True):
        return self._path

    def docs_iter(self):
        fields = ", ".join(self._doc_cls._fields)
        results = con.query(f"SELECT id, url, main_content, title, description FROM {self._path};")

        while batch := results.fetchmany():
            for row in batch:
                row["doc_id"] = row["id"]
                row["main_content"] = ir_datasets.util.sax_html_parser(row["main_content"], fields=[None])[0]
                yield self._doc_cls(*row)

    def docs_cls(self):
        return self._doc_cls

    def docs_count(self):
        return con.query(f"SELECT COUNT(*) FROM {self._path};").fetchone()[0]


class ParquetDocstore(Docstore):
    def __init__(self, path, doc_cls, id_field='doc_id'):
        super().__init__(doc_cls, id_field)
        self._path = path

    def get_many_iter(self, doc_ids):
        fields = ", ".join(self._doc_cls._fields)
        results = con.query(f"SELECT {fields} FROM {self._path} WHERE {self._id_field} IN ?;", params=[tuple(doc_ids)])

        while batch := results.fetchmany():
            for row in batch:
                yield self._doc_cls(*row)


def register_to_ir_datasets():
    from ir_datasets import registry
    docs = ParquetDocs("read_parquet('s3://ir-teach-wise-2025/*.parquet')", doc_cls=OWIDoc)
    registry.register("wows/owi/2025", Dataset(docs))


if __name__ == '__main__':
    store = ParquetDocstore("read_parquet('s3://ir-teach-wise-2025/*.parquet')", doc_cls=OWIDoc, id_field="id")

    docs_to_collect = set()
    import pandas as pd
    for doc_id in pd.read_csv('../collection/manual.csv')['doc_id']:
        docs_to_collect.add(doc_id)

    docs = {}

#    for run in glob('../collection/runs/*'):
#        parsed_run = pd.read_csv(run, header=0, names=['qid', 'q0', 'doc_id', 'rank', 'score', 'system'], sep=" ")
#        for doc_id in parsed_run['doc_id']:
#            docs_to_collect.add(doc_id)

    print(len(docs_to_collect))

    with gzip.open('corpus.jsonl.gz', 'wt') as f:
        for doc in tqdm(store.get_many_iter(docs_to_collect)):
            default_text = ''
            if doc.title:
                default_text += ' ' + doc.title
            if doc.main_content:
                default_text += ' ' + doc.main_content
            if doc.description:
                default_text += ' ' + doc.description

            f.write(json.dumps({"doc_id": doc.id, "url": doc.url, "default_text":  default_text.strip(), "main_content": doc.main_content, "title": doc.title, "description": doc.description}) + '\n')
            f.flush()

    #print(docs.docs_count())

    #for doc in docs.docs_iter():
    #    print(doc)
    #    break

    #print(store.get("00000072d6e64d4a5e05fabdb1fa94ee06cd30e697163ba12ae22f2771026465"))
