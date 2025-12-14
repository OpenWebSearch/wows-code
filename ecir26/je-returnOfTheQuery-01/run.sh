#!/bin/bash
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model BM25 --text-field-to-retrieve default_text
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model PL2 --text-field-to-retrieve default_text
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model DirichletLM --text-field-to-retrieve default_text

./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model BM25 --text-field-to-retrieve title
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model PL2 --text-field-to-retrieve title
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model DirichletLM --text-field-to-retrieve title

./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model BM25 --text-field-to-retrieve description
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model PL2 --text-field-to-retrieve description
./retrieve.py --dataset radboud-validation-20251114-training --output best-try --retrieval-model DirichletLM --text-field-to-retrieve description