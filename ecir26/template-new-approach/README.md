# PyTerrier Baseline


Get an overview of all possibilities to execute this baseline via:

```
./retrieve.py --help
```

This should yield an output like:

```
Usage: retrieve.py [OPTIONS]

Options:
  --dataset [radboud-validation-20251114-training|spot-check-20251122-training]
                                  The dataset.  [required]
  --output PATH                   The output directory.  [required]
  --retrieval-model TEXT          The retrieval model.
  --index [default|title|description]
                                  The text field of the index on which to
                                  retrieve.
  --help                          Show this message and exit.
```

## Upload some run via:

```
tira-cli upload --directory DIRECTORY-WITH-RUN
```

## Run All Variants

We run retrieval via:

```
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model BM25 --index default
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model PL2 --index default
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model DirichletLM --index default

./retrieve.py --dataset DATASET-ID --output runs --retrieval-model BM25 --index title
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model PL2 --index title
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model DirichletLM --index title

./retrieve.py --dataset DATASET-ID --output runs --retrieval-model BM25 --index description
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model PL2 --index description
./retrieve.py --dataset DATASET-ID --output runs --retrieval-model DirichletLM --index description
```

## Indexing

Submit the indexing as code submission to tira

```
tira-cli code-submission \
    --path . \
    --task ir-lab-wise-2025 \
    --tira-vm-id ows \
    --dataset spot-check-20251122-training \
    --command '/index.py --dataset $inputDataset --output $outputDir/index --text-field default_text' \
    --dry-run
```
