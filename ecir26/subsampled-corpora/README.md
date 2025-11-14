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

