from conf import settings as s
import pandas as pd
import utils as ut

df_ct = ut.get_df(s.clinical_trials_file, {'index_col': 0})
df_dr = ut.get_df(s.drugs_file, {'index_col': 0})
df_pub = ut.get_df(s.pubmed_file, {'index_col': 0})
