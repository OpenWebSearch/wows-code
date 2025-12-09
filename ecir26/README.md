# Submission Instructions

This directory contains example submissions.

We use [TIRA.io](https://www.tira.io/task-overview/ir-lab-wise-2025) for submissions, you can either make run submissions (i.e., upload run files, e.g., via the command line) or optionally software submissions. We aim to collaboratively develop and prepare a set of [PyTerrier Artifacts](https://dl.acm.org/doi/abs/10.1145/3726302.3730147) for the datasets we collaboratively develop. An overview (currently in alpha development stage) of the available artifacts is available at [tira.io/tirex/pyterrier-artifacts-beta?query=ir-lab-wise-2025](https://www.tira.io/tirex/pyterrier-artifacts-beta?query=ir-lab-wise-2025).


## Available Datasets

All datasets that we developed collaboratively are (while they are in progress, as soon as everything is finalized we will also mirror them to Zenodo properly) listed at [tira.io/datasets?query=ir-lab-wise-2025](https://www.tira.io/datasets?query=ir-lab-wise-2025).

At the moment, the datasets are:

- `spot-check-20251122-training`: A tiny spot check dataset so that you can fastly ensure your approach gives valid outputs.
- `radboud-validation-20251114-training`: A validation dataset created in the Radboud IR course.

Additionally, two test datasets are currently under construction, one created in the Radboud IR course, and one created in the Jena/Kassel IR courses.


## Run Submissions

Submissions are expected to have the following structure:

```
├── ir-metadata.yml
└── run.txt.gz
```

The `ir-metadata.yml` file describes your approach in the [ir-metadata format](https://www.ir-metadata.org/) and the `run.txt.gz` file is a standard TREC-style run file for the dataset.

The directory [submission-skeleton](submission-skeleton) contains an example (please replace all `ENTER_VALUE_HERE` occurences in the ir-metadata.yml file of the skeleton with your actual data to make it valid).


You can verify and submit your submission via `tira-cli`.

1. Install the tira client via:

```
pip3 install --upgrade tira
```

2. Verify your submission (i.e., the `--dry-run` flag):

```
tira-cli upload --dry-run --directory submission-skeleton
```

For valid submissions, the output should look like:

<img width="968" height="183" alt="Screenshot_20251123_192741" src="https://github.com/user-attachments/assets/7498f0d6-8442-4e06-82e1-3a8508a524b6" />

If `tira-cli upload --dry-run --directory submission-skeleton` fails, log in first via your token from TIRA.io submission page.

3. Upload your submission (i.e., remove the `--dry-run` flag and login):

```
# First login via your token from TIRA.io submission page
tira-cli login --token YOUR-TOKEN-FROM-TIRA-IO
tira-cli upload --directory web-submission-skeleton
```

## Approaches

We aim to maintain all work here in a mono-repository to have everything at one place. Therefore, we want to collect all approaches as directories in this repository. If you have a new approach, please add them via a pull request (i.e., fork the repository, and then, as soon as your approach is "finished enough", please create a pull request that adds your approach as a new directory, you do not need to add all your approaches, but the ones that you think could be interesting for others as well).

If you want to add a new approach, please develop it in a [dev container](https://containers.dev/), as this makes it easier for others to run your approach.
When doing so, ensure that you open your IDE in a subdirectory that contains **only one** dev-container specification, so that the correct container can be started.

We have a set of baseline approaches that you can take as inspiration:

- [pyterrier-baseline](pyterrier-baseline) provides a minimal baseline that loads PyTerrier indexes as Artifacts and should therefore be the fastest approach to get something to run.
- [template-new-approach](template-new-approach) does everything from scratch (i.e., without artifacts), so that you have full control over every potential aspect that you might want to modify. Please use this directory as starting point for new approaches.
- [chatnoir-baseline](chatnoir-baseline) does baseline retrieval with [ChatNoir](https://www.chatnoir.eu/).


We want to improve the re-usability of experimental artifacts with the [PyTerrier Artifacts](https://dl.acm.org/doi/abs/10.1145/3726302.3730147) paradigm, therefore, please have a look at the [corresponding tutorial](https://github.com/tira-io/teaching-ir-with-shared-tasks/blob/main/tutorials/tutorial-pyterrier-artifacts.ipynb) so that you get a feeling on how to use them. Ideally, if you have an idea of experimental artifacts that you think others could also use, please do not hesitate to make them available (e.g., as upload to tira makes them available).

