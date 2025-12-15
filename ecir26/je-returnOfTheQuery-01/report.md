# Retrieval System - Return of the Query

## Indexing

Lorem Ipsum

## Reranking

In der parallel laufenden Vorlesung wurde **Reranking** als erste Verbesserung eines bestehenden Systems vorgeschlagen. 

Beim Reranking wird das Ergebnis eines bestehenden Retrieval-Systems mit einem anderen, teureren System verglichen, um es zu verbessern. Der Begriff „teuer” bezieht sich hierbei auf die Computing-Kosten, die das System verursacht. In der Regel ist durch die höheren Kosten ein besseres Ergebnis zu erwarten. Um den Aufwand jedoch in einem gewissen Rahmen zu halten, wird nicht das gesamte Ergebnis neu bewertet, sondern nur ein Teil davon. Typischerweise wird auf den ersten 100 Ergebnissen rerankt und, falls erneut rerankt wird, auf den ersten 5 bis 50.

### Learning to Rank (LTR)

Es gibt verschiedene Ansätze, um das Retrieval zu erlernen. Dabei gibt es drei Ziele.

- **Pointwise LTR**: Es werden die Scores der Dokumente für jedes Dokument individuell vorhergesagt. Bei der Pointwise LTR wird [monoT5 [Nogueira et al., 2020]](https://arxiv.org/pdf/2003.06713) genutzt. 

- **Pairwise LTR**: Es werden "präfferenzen" für Paare von Doumenten vorhergesagt. Es wird [duoT5 [Pradeep et al., 2021]](https://arxiv.org/pdf/2101.05667) genutzt.

- **Listwise LTR**: Es wird ein Rank effektivitäts Measure optimiert. Dies ist nach Stand der vorlesung noch nicht implementiert.

Ein typischer Ansatz für eine Reranking-Pipeline ist der folgende:
1. BM25-Ranking auf der kompletten Sammlung,
2. Pointwise Reranking der Top-100-Ergebnisse.
3. Pairwise Reranking der Top 50 Ergebnisse aus Schritt 2.
4. Ranking nach dem aggregierten Score aus Schritt 3.

Dieser Ansatz wird auch in unserem System mit anderen Top-Score-Ergebnissen verwendet.

### Code

Um das Rad nicht neu zu erfinden, nutzen wir die Python-Retrieval-Bibliothek [Pyterrier](https://github.com/terrier-org/pyterrier.git). Pyterrier bietet viele bereits implementierte und optimierte Retrieval-Methoden und -Ansätze. Standardmäßig ist BM25 enthalten.

Pointwise-Modelle sind verfügbar, Pairwise-Modelle jedoch nicht. Dafür gibt es die Bibliothek [Pyterrier T5](https://github.com/terrierteam/pyterrier_t5?tab=readme-overview). Diese implementiert die monoT5- und die duiT5-Modelle sowie die Pointwise- und die Pairwise-Modelle. Diese können direkt genutzt werden.

```python
import pyterrier
import pyterrier_t5

# Initialisierung der Retrival Modelle
# Für die einfachheit, wird der Index nicht definiert.
bm25 = pt.terrier.Retriever(index, wmodel="BM25")
reranker_pointwise = MonoT5ReRanker()
reranker_pairwise = DuoT5ReRanker()
```

In Pyterrier gibt es verschiedene Operatoren, mit denen sich Aussagen vereinfachen lassen. Ein Beispiel ist der Operator [>>](https://pyterrier.readthedocs.io/en/latest/operators.html#then). Dieser ermöglicht die Erstellung von Pipelines und somit die übersichtliche Definition mehrerer Arbeitsschritte hintereinander in einer Zeile.

```python
# Rerank Pipeline
mono_pipeline = retriever % 100 >> reranker_pointwise
duo_pipeline = mono_pipeline % 5  >> reranker_pairwise
run = duo_pipeline.transform(topics)
```

### Ergebnis

Zu Beginn haben wir die Baseline des Systems mit einem BM25-Retrieval-System gemessen. Als Gütemaß haben wir NDCG@10 gewählt. Dieser Wert wurde für alle berechnet und anhand dessen wurden die Vergleiche durchgeführt.

||Modell|  ndcg@10|
|-|-|-|
|-|Baseline BM25|0.451635|
|0|                pyterrier-PL2-on-title-3| 0.263840|
|1|               pyterrier-BM25-on-title-3| 0.274660|
|2|        pyterrier-DirichletLM-on-title-3| 0.110035|
|3| pyterrier-DirichletLM-on-default_text-3| 0.247526|
|4|  pyterrier-DirichletLM-on-description-3| 0.065785|
|5|         pyterrier-BM25-on-description-3| 0.162492|
|6|        pyterrier-BM25-on-default_text-3| 0.317093|
|7|         pyterrier-PL2-on-default_text-3| 0.346148|
|8|          pyterrier-PL2-on-description-3| 0.139911|

Wie in der Tabelle zu sehen ist, wurden die Baseline-Werte unterschritten. Das System hat sich durch das Reranking nicht verbessert, sondern verschlechtert. Die Gründe dafür können wir uns derzeit nicht erklären.

## Contributers

Team: Return of the Query
- [Moritz Raetz](mailto:moritz.raetz@uni.jena.de)
- [Leonard Teschner](mailto:leonard.teschner@uni-jena.de)

Text mit [Deepl.com/write](https://www.deepl.com/de/write) umgeschrieben.