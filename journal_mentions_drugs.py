import pandas as pd
from drugs_graph.conf import settings as s

df_res = pd.read_json(s.results_path / s.output_file)

series_journal = df_res.loc['journal']
list_dict_journal = series_journal.to_list()
list_all_journal = []

for d in list_dict_journal:
    list_all_journal += list(d.keys())

res = max(list_all_journal, key=list_all_journal.count)

print(f"The journal that mentions the most drugs is: {res}")
