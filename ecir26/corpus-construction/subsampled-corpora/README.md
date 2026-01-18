# Subsampled Corpora

We apply [corpus subsampling]() to allow for Green experimentation using the subsampling implementation of the [lsr-benchmark](https://github.com/reneuir/lsr-benchmark/).

The subsamples are created via:

```
lsr-benchmark create-lsr-corpus radboud-validation
```

Then, upload the subsamples to TIRA via:

```
tira-cli dataset-submission --path radboud-validation/ --task ir-lab-wise-2025 --split train
```

## Spot Check

There exists a tiny spot-check dataset that you can use to verify that your approaches work.

```
tira-cli dataset-submission --path spot-check/ --task ir-lab-wise-2025 --split train
```

