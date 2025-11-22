# PyTerrier Baseline


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
