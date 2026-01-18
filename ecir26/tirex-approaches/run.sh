#!/usr/bin/env bash

./run-tirex-approach.py --tira-approach "tira-ir-starter/DFIZ Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfiz --tag dfiz-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFIZ Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dfiz --tag dfiz-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFRee Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output output/dfree --tag dfree-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DFReeKLIM Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dree-kl --tag dfree-kl-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DirichletLM Re-Rank (tira-ir-starter-pyterrier)"  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dirichlet --tag dirichlet-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DLH Re-Rank (tira-ir-starter-pyterrier)" --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dlh --tag dlh-re-ranker
./run-tirex-approach.py --tira-approach "tira-ir-starter/DPH Re-Rank (tira-ir-starter-pyterrier)",  --dataset ir-lab-wise-2025/radboud-validation-20251114-training --output output/dph --tag dph-re-ranker
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

