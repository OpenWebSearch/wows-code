#!/usr/bin/env python3
from glob import glob
import json
from tqdm import tqdm
import gzip
import uuid
from pathlib import Path

DATA_DIR = '/mnt/ceph/storage/data-in-progress/data-research/web-search/wows25/'


def parse_qrel(labels):
    if labels == ['Not Relevant (0)']:
        return 0
    elif labels == ['Relevant (1)']:
        return 1
    elif labels == ['Highly Relevant (2)']:
        return 2
    raise ValueError('foo')

def load_qrels():
    ret = {}
    for annotation_file in tqdm(glob(f'{DATA_DIR}/truth-data/*')):
        with open(annotation_file, 'r') as f:
            for l in f:
                l = json.loads(l)
                if l['query_id'] not in ret:
                    ret[l['query_id']] = {}

                label = parse_qrel(l['label'])
                assert l['passage_id'] not in ret[l['query_id']], (l['passage_id'])
                ret[l['query_id']][l['passage_id']] = label
    return ret

def load_pairwise_files(qrels):
    ret = []

    qrels_covered = {}
    for pairwise_file in tqdm(glob(f'{DATA_DIR}/inputs/*')):
        with gzip.open(pairwise_file, 'r') as f:
            for l in f:
                pair_id = str(uuid.uuid4())
                l = json.loads(l)
                query_id = l['qid']
                if type(l['known_relevant_passage']) == str:
                    continue
                query = l['query_text']
                relevant_doc_id = l['known_relevant_passage']['docno']
                relevant_doc = l['known_relevant_passage']['text']
                unknown_doc_id = l['passage_to_judge']['docno']
                unknown_doc = l['passage_to_judge']['text']

                if unknown_doc_id not in qrels[query_id]:
                    continue

                if query_id not in qrels_covered:
                    qrels_covered[query_id] = set()
                qrels_covered[query_id].add(unknown_doc_id)
                ret.append({
                    "id": pair_id,
                    "query": query,
                    "query_id": str(query_id),
                    "relevant": relevant_doc,
                    "relevant_doc_id": str(relevant_doc_id),
                    "unknown": unknown_doc,
                    "unknown_doc_id": str(unknown_doc_id),
                    "qrel_unknown_doc": qrels[query_id][unknown_doc_id],
                    "source_dataset_id": l['source_dataset_id'],
                })

    preds = 0
    for q in qrels.keys():
        for docid in qrels[q].keys():
            preds += 1
            if q not in qrels_covered or docid not in qrels_covered[q]:
                raise ValueError('-->', q, docid)
    print('Preds ' + str(preds) + ' -> ' + str(len(ret)))
    return ret

qrels = load_qrels()
pairwise_data = load_pairwise_files(qrels)

Path(f'{DATA_DIR}/zenodo/test-pairwise/truths/').mkdir(parents=True, exist_ok=True)
Path(f'{DATA_DIR}/zenodo/test-pairwise/inputs/').mkdir(parents=True, exist_ok=True)
Path(f'{DATA_DIR}/zenodo/test-pointwise/truths/').mkdir(parents=True, exist_ok=True)
Path(f'{DATA_DIR}/zenodo/test-pointwise/inputs/').mkdir(parents=True, exist_ok=True)

with open(f'{DATA_DIR}/zenodo/test-pairwise/truths/inputs.jsonl', 'w') as f:
    for l in pairwise_data:
        f.write(json.dumps(l) + '\n')

with open(f'{DATA_DIR}/zenodo/test-pairwise/inputs/inputs.jsonl', 'w') as f:
    for l in pairwise_data:
        del l['source_dataset_id']
        del l['query_id']
        del l['relevant_doc_id']
        del l['unknown_doc_id']
        del l['qrel_unknown_doc']

        f.write(json.dumps(l) + '\n')

pointwise_data = []
covered_ids = set()

with open(f'{DATA_DIR}/zenodo/test-pairwise/truths/inputs.jsonl', 'r') as f:
    for l in f:
        l = json.loads(l)
        if l['unknown_doc_id'] in covered_ids:
            continue

        covered_ids.add(l['unknown_doc_id'])
        l['id'] = str(uuid.uuid4())
        del l['relevant']
        del l['relevant_doc_id']
        pointwise_data.append(l)

with open(f'{DATA_DIR}/zenodo/test-pointwise/truths/inputs.jsonl', 'w') as f:
    for l in pointwise_data:
        f.write(json.dumps(l) + '\n')

with open(f'{DATA_DIR}/zenodo/test-pointwise/inputs/inputs.jsonl', 'w') as f:
    for l in pointwise_data:
        del l['source_dataset_id']
        del l['query_id']
        del l['unknown_doc_id']
        del l['qrel_unknown_doc']
        f.write(json.dumps(l) + '\n')
