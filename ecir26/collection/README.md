# Labeling Step By Step

We configured the pooling so that the number of documents is on mean and on median slighly below 50 (mean: 47.7, median 46.5).

- Go to [https://doccano.web.webis.de](https://doccano.web.webis.de)
- Click on login, enter your credentials
- You see a single project (named after your account), click on it, then click on "Start Annotation"

# Setting Up Doccano Step by Step

## 1. Install teaching-ir locally

Step 1: clone the repository:

```
git clone git@github.com:tira-io/teaching-ir-with-shared-tasks.git
```

cd into the directory, and install it:

```
pip3 install --no-deps -e . --break-system-packages
```

Check it works:

```
teaching-ir --help
```

## 2. Run pooling

After playing around a bit, we decided to choose a depth of 11 for the pooling.

```
teaching-ir pool-documents --pooling-depth 11 .
```

## 3. Upload to Doccano

```
teaching-ir prepare-relevance-judgments --doccano-url https://doccano.web.webis.de/ --doccano-username admin --doccano-password TODO wows doccano-judgment-pool.jsonl
```

## 4. Export QRELS

```
teaching-ir export-relevance-judgments --doccano-url https://doccano.web.webis.de/ --doccano-username admin --doccano-password TODO wows .
``
