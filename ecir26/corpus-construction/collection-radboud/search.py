import random
import pyterrier as pt
import pandas as pd


df = pd.read_csv("topics.csv")

topics = df[df["selected"] | df["additional"]][["title", "description", "narrative", "snumber"]].rename(columns={"title": "query", "snumber": "author"}).sample(frac=1)
topics["qid"] = range(1, len(topics) + 1)

print(topics)

topics[["qid", "author"]].to_csv("authors.csv", index=False)

topics.drop(columns=["author"], inplace=True)

topics.to_csv("topics-final.csv", index=False)


for representation in ["title", "description", "content"]:
    print(representation)
    index = pt.IndexFactory.of(f"./index-{representation}", memory=representation != "content")

    for wmodel in ["BM25", "PL2", "Hiemstra_LM"]:
        print(wmodel)

        retr = pt.rewrite.tokenise() >> pt.terrier.Retriever(index, wmodel=wmodel, properties={"termpipelines": ""})

        run = retr.transform(topics)

        pt.io.write_results(run, f"runs/ows-{representation}-{wmodel.lower().replace('_', '')}.txt.gz")
