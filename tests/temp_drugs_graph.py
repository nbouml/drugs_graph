import pandas as pd
from pathlib import Path

DATA_FOLDER = Path(__file__, fs="local").parent.parent / "data"
df_ct = pd.read_csv(DATA_FOLDER / "clinical_trials.csv", index_col=0)
df_dr = pd.read_csv(DATA_FOLDER / "drugs.csv", index_col=0)
df_pub = pd.read_csv(DATA_FOLDER / "pubmed.csv", index_col=0)

print(df_pub)

# data prep to lowercase
# TODO f1 : if id is nan : if two items match with another id then merge them
# TODO f2 : drop duplicates in : df_ct
# TODO f3 : convert columns date to datetime : pd.to_datetime(df_ct['date'], dayfirst=True)
df_dr = df_dr.apply(lambda x: x.str.lower())

# 1er rule:  find drug name in the title
# TODO f1 : convert columns to lower string
#
drug_name = "diphenhydramine"
in_pub = df_pub['title'].str.lower().str.find(drug_name)
in_ct = df_ct['scientific_title'].str.lower().str.find(drug_name)

# output
res = {
    "title": "drug_name",
    "type": "object",
    "properties":
        {
            "pubmed":
                {"id1": "date",
                 "id2": "date"},
            "clinical trials":
                {"id1": "date",
                 "id2": "date"},
            "journal":
                {"id1": "date",
                 "id2": "date"}

        }
}

print(res)
