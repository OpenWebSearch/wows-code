## Research Homework

**Research Question:**
Can an MS-MARCO-trained Cross-Encoder Reranker, combined with score interpolation, significantly improve retrieval effectiveness on the Radboud dataset compared to a standard BM25 baseline?

<hr>

**Hypothesis 1:**

There is a statistically significant difference in mean nDCG@10 scores on the radboud-validation-20251114-training dataset between the standard BM25 pipeline and the pipeline extended with the ms-marco-MiniLM-L-6-v2 reranker (re-ranking the top-50 documents with linear score interpolation, $\alpha=0.1$). (two-sided t-test with $\alpha=0.05$)
<hr>

**Null Hypothesis 1:**

There is no statistically significant difference in mean nDCG@10 scores on the radboud-validation-20251114-training dataset between the standard BM25 pipeline and the pipeline extended with the ms-marco-MiniLM-L-6-v2 reranker (re-ranking the top-50 documents with linear score interpolation, $\alpha=0.1$). (two-sided t-test with $\alpha=0.05$)
<hr>

**Hypothesis 2:**

The pipeline extended with the ms-marco-MiniLM-L-6-v2 reranker (re-ranking the top-50 documents with linear score interpolation, $\alpha=0.1$) achieves a statistically significant improvement in mean nDCG@10 scores on the radboud-validation-20251114-training dataset compared to the standard BM25 pipeline. (one-sided t-test with $\alpha=0.05$)
<hr>

**Null Hypothesis 2:**

The pipeline extended with the ms-marco-MiniLM-L-6-v2 reranker (re-ranking the top-50 documents with linear score interpolation, $\alpha=0.1$) achieves no statistically significant improvement in mean nDCG@10 scores on the radboud-validation-20251114-training dataset compared to the standard BM25 pipeline. (one-sided t-test with $\alpha=0.05$)

