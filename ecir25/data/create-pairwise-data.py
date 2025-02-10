#!/usr/bin/env python3
from tira.third_party_integrations import ir_datasets
import uuid
import json

dataset = ir_datasets.load('ir-lab-wise-2024/subsampled-ms-marco-deep-learning-20241201-training')

def browse_dataset(dataset):
    qid_to_rel = {}

    for qrel in dataset.qrels_iter():
        if qrel.query_id not in qid_to_rel:
            qid_to_rel[qrel.query_id] = {}

        if qrel.relevance not in qid_to_rel[qrel.query_id]:
            qid_to_rel[qrel.query_id][qrel.relevance] = 0

        qid_to_rel[qrel.query_id][qrel.relevance] += 1

    for query in dataset.queries_iter():
        print(query.query_id, '->', query.title, qid_to_rel[query.query_id])



def select_qrels(dataset, qid, target_relevance):
    for qrel in dataset.qrels_iter():
        
        if str(qrel.query_id) == str(qid) and qrel.relevance == target_relevance:
            print(qrel)

def calculate_pairwise_data(qid_to_split, dataset):
    qid_to_inference_pairs = {}
    qid_to_query = {}
    qid_to_doc_to_rel = {}
    docs_store = dataset.docs_store()

    for query in dataset.queries_iter():
        qid_to_query[query.query_id] = query.default_text()

    for qrel in dataset.qrels_iter():
        if str(qrel.query_id) not in qid_to_doc_to_rel:
            qid_to_doc_to_rel[str(qrel.query_id)] = {}

        qid_to_doc_to_rel[str(qrel.query_id)][str(qrel.doc_id)] = qrel.relevance

    for qid in qid_to_split:
        for training_doc in qid_to_split[qid]['training']:
            for test_doc in qid_to_split[qid]['test']:
                if test_doc in qid_to_split[qid]['training']:
                    raise ValueError('foo')

                if (training_doc, test_doc) in qid_to_inference_pairs:
                    raise ValueError('foo')
                
                qid_to_inference_pairs[(training_doc, test_doc)] = {
                    'id': str(uuid.uuid4()),
                    'query': qid_to_query[str(qid)],
                    'query_id': qid,
                    'relevant': docs_store.get(training_doc).default_text(),
                    'relevant_doc_id': training_doc,
                    'unknown': docs_store.get(test_doc).default_text(),
                    'unknown_doc_id': test_doc,
                    'qrel_unknown_doc': qid_to_doc_to_rel[str(qid)][str(test_doc)]
                }

    return qid_to_inference_pairs

def persist_data_pairwise(qid_to_split, dataset):
    qid_to_inference_pairs = calculate_pairwise_data(qid_to_split, dataset)

    with open('smoke-test-dataset/pairwise/inputs/inputs.jsonl', 'w') as input_file, open('smoke-test-dataset/pairwise/labels/labels.jsonl', 'w') as labels_file:
        for training_doc, test_doc in qid_to_inference_pairs.keys():
            i = qid_to_inference_pairs[(training_doc, test_doc)].copy()
            t = qid_to_inference_pairs[(training_doc, test_doc)].copy()

            del i['query_id']
            del i['relevant_doc_id']
            del i['unknown_doc_id']
            del i['qrel_unknown_doc']

            input_file.write(json.dumps(i) + '\n')
            labels_file.write(json.dumps(t) + '\n')

def persist_data_pointwise(qid_to_split, dataset):
    qid_to_inference_pairs = calculate_pairwise_data(qid_to_split, dataset)
    covered_ids = set()
    with open('smoke-test-dataset/pointwise/inputs/inputs.jsonl', 'w') as input_file, open('smoke-test-dataset/pointwise/labels/labels.jsonl', 'w') as labels_file:
        for training_doc, test_doc in qid_to_inference_pairs.keys():
            i = qid_to_inference_pairs[(training_doc, test_doc)].copy()
            t = qid_to_inference_pairs[(training_doc, test_doc)].copy()

            if i['unknown_doc_id'] in covered_ids:
                continue

            covered_ids.add(i['unknown_doc_id'])


            del t['relevant_doc_id']
            del t['relevant']
            del i['query_id']
            del i['relevant_doc_id']
            del i['relevant']
            del i['unknown_doc_id']
            del i['qrel_unknown_doc']

            input_file.write(json.dumps(i) + '\n')
            labels_file.write(json.dumps(t) + '\n')


QID_TO_SPLITS = {
    # who sings monk theme song {0: 100, 2: 7, 1: 30, 3: 3}
    1051399: {
        'training': set(['2530579', '3943228', '69813']),
        'test': set(['7865069', '4642930', '3376628', '5040048', '3108511', '2378828', '4426187'])
    },

    833860: {
        'training': set(['5167510', '2206197', '115142']),
        'test': set(['1889863', '7831470', '45135', '6943600', '7103434', '2830558']),
    }
}

if __name__ == '__main__':
    persist_data_pairwise(QID_TO_SPLITS, dataset)
    persist_data_pointwise(QID_TO_SPLITS, dataset)
    # print('foo')
    # select_qrels(dataset, 833860, 0)
    print('finished')
