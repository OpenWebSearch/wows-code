#!/usr/bin/env python3
import pandas as pd
from statistics import mean

EXCLUSION_TOPIC_IDS = set(["3", "4", "7", "8", "13", "15", "16", "18", "20", "23", "24", "31", "32", "34", "39", "42", "43", "44", "46", "48", "52", "54", "58", "60", "64", "68", "69", "74"])

topics = pd.read_csv("topics-final.csv")
reformatted_topics = []

for _, topic in topics.iterrows():
    if str(topic["qid"]) in EXCLUSION_TOPIC_IDS:
        continue
    reformatted_topics.append(f'<topic number="{topic["qid"]}">\n  <num>{topic["qid"]}</num><title>{topic["query"]}</title>\n  <description>{topic["description"]}</description>\n  <narrative>{topic["narrative"]}</narrative>\n</topic>\n')

assert len(reformatted_topics) == len(topics) - len(EXCLUSION_TOPIC_IDS)

with open("../subsampled-corpora/radboud-test/topics.xml", "wt") as f:
    f.write("<topics>\n" + ("".join(reformatted_topics)) + "\n</topics>")

qid_to_doc_to_judgments = {}
qrels_raw = pd.read_json("raw-exported-doccano-judgments.jsonl", lines=True)

for _, i in qrels_raw.iterrows():
    qid = str(i["query_id"])
    docid = str(i["doc_id"])
    if qid in EXCLUSION_TOPIC_IDS:
        continue

    if qid not in qid_to_doc_to_judgments:
        qid_to_doc_to_judgments[qid] = {}
    if docid not in qid_to_doc_to_judgments[qid]:
        qid_to_doc_to_judgments[qid][docid] = []

    for label in i["label"]:
        qid_to_doc_to_judgments[qid][docid].append(int(label.split("(")[-1].split(")")[0]))

assert len(qid_to_doc_to_judgments.keys()) == len(topics) - len(EXCLUSION_TOPIC_IDS)

with open("../subsampled-corpora/radboud-test/qrels.txt", "wt") as f:
    for qid in qid_to_doc_to_judgments.keys():
        for docid in qid_to_doc_to_judgments[qid].keys():
            labels = qid_to_doc_to_judgments[qid][docid]
            if len(labels) == 0:
                continue
            label = int(mean(labels))
            f.write(f"{qid} 0 {docid} {label}\n")
