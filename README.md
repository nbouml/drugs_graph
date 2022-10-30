[![doc](https://img.shields.io/badge/-Documentation-blue)](https://nbouml.github.io/drugs_graph/)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/badge/python-3.9-blue.svg)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/noureddine-boumlaik-0835a960/)
[![mail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:boum.nour19@gmail.com)

# Usage

To run the code with docker you have to build the image: 
`make build` and run it with: `make run`. 
The result will saved in `DRUGS_GRAPH_RESULTS_PATH`

# Drugs graph

graph of the link between the different drugs and their respective mentions in the different PubMed publications, 
the different scientific publications and finally the journals with the date associated with each of these mentions.
The representation below allows to visualize what is expected.

Business Rules:
* A drug is considered mentioned in a PubMed article or clinical trial if it is mentioned in the title of the publication.
* A drug is considered as mentioned by a journal if it is mentioned in a publication issued by this journal.


![alt text](https://github.com/nbouml/drugs_graph/blob/master/img/dgrap.png)

# Architecture

In `data` we have the raw project files, and two directories, `base` and `results`.
In `base` we save the temporary files, and the final result will be saved in `results`.
The configuration and methods are located in `drugs_graph/conf` and `drugs_graph/src`.
The `img` repository is for documentation images.

# Configuration

```
DRUGS_GRAPH_INPUT_DATA_PATH=data
DRUGS_GRAPH_BASE_PATH=data/base
DRUGS_GRAPH_RESULTS_PATH=data/results

DRUGS_GRAPH_CLINICAL_TRIALS_FILE=clinical_trials.csv
DRUGS_GRAPH_DRUGS_FILE=drugs.csv
DRUGS_GRAPH_PUBMED_FILE=pubmed.csv
DRUGS_GRAPH_JOURNALS_FILE=journals.csv
DRUGS_GRAPH_OUTPUT_FILE=graph.json

DRUGS_GRAPH_COLS_REF_CT="scientific_title,date"

DRUGS_GRAPH_DAG_TITLE_STR=title
DRUGS_GRAPH_DAG_DRUG_STR=drug
DRUGS_GRAPH_DAG_JOURNAL_STR=journal
DRUGS_GRAPH_DAG_PUBMED_STR=pubmed
DRUGS_GRAPH_DAG_CLINICAL_TRIALS_STR=clinical_trials
DRUGS_GRAPH_DAG_DATE_STR=date
DRUGS_GRAPH_DAG_SCIENTIFIC_TITLE=scientific_title

DRUGS_GRAPH_ENGINE=memory
```