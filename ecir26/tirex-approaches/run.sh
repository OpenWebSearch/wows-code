#!/usr/bin/env bash

./run-tirex-approach.py --tira-approach "tira-ir-starter/DFIZ Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfiz --tag dfiz-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFIZ Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfiz --tag dfiz-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFRee Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfree --tag dfree-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFReeKLIM Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dree-kl --tag dfree-kl-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DirichletLM Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dirichlet --tag dirichlet-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DLH Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dlh --tag dlh-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DPH Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dph --tag dph-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/Hiemstra_LM Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/hiemstra --tag hiemstra-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/IFB2 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/ifb2 --tag ifb2-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/In_expB2 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/in-expb2 --tag in-expb2-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/In_expC2 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/in-expc2 --tag in-expc2-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/InB2 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/in-b2 --tag in-b2-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/Js_KLs Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/js-kls --tag js-kls-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/LGD Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/lgd --tag lgd-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/PL2 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/pl2 --tag pl2-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/TF_IDF Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/tf-idf --tag tf-idf-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/XSqrA_M Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/xsqram --tag xsqram-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFR_BM25 Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfr-bm25 --tag dfr-bm25-re-rankre


./run-tirex-approach.py --gpu 0 --tira-approach "naverlabseurope/Splade (re-ranker)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/splade --tag splade
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/ColBERT Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/colbert --tag colbert
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/MonoT5 Base (tira-ir-starter-gygaggle)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/monot5-base --tag monot5-base
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/ANCE Base Cosine (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/ance-cosine --tag ance-cosine
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/ANCE Base Dot (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/ance-dot --tag ance-dot
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/SBERT msmarco-distilbert-base-v3-cos (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/distilbert-v3-cos --tag distilbert-v3-cos
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/SBERT msmarco-distilbert-base-v3-dot (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/distilbert-v3-dot --tag distilbert-v3-dot
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/SBERT msmarco-MiniLM-L6-cos-v5 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/minilm-l6-v5 --tag minilm-l6-v5
./run-tirex-approach.py --gpu 0 --tira-approach "tira-ir-starter/SBERT msmarco-MiniLM-L12-cos-v5 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/minilm-l12-v5 --tag minilm-l12-v5


./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT msmarco-distilbert-cos-v5 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/distilbert-cos-v5 --tag distilbert-cos-v5
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT msmarco-distilbert-dot-v5 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/distilbert-dot-v5 --tag distilbert-dot-v5
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT msmarco-bert-base-dot-v5 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/bert-base-dot-v5 --tag bert-base-dot-v5
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/TASB msmarco-distilbert-base-cos (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/tasb-cos --tag tasb-cos
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/TASB msmarco-distilbert-base-dot (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/tasb-dot --tag tasb-dot
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-MiniLM-L6-cos-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/minilm-l6-cos-v1 --tag minilm-l6-cos-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-distilbert-cos-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/distilbert-cos-v1 --tag distilbert-cos-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-mpnet-base-cos-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/mpnet-cos-v1 --tag mpnet-cos-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-MiniLM-L6-dot-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/qa-minilm-l6-dot-v1 --tag qa-minilm-l6-dot-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-distilbert-dot-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/qa-distilbert-dot-v1 --tag qa-distilbert-dot-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/SBERT multi-qa-mpnet-base-dot-v1 (tira-ir-starter-beir)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/qa-mpnet-dot-v1 --tag qa-mpnet-dot-v1
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/MonoBERT Base (tira-ir-starter-gygaggle)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/monobert-base --tag monobert-base
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/MonoBERT Small-MS-MARCO-10k (tira-ir-starter-gygaggle)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/monobert-small-10k --tag monobert-small-10k
./run-tirex-approach.py --gpu 1 --tira-approach "tira-ir-starter/MonoBERT Small (tira-ir-starter-gygaggle)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/monobert-small --tag monobert-small
