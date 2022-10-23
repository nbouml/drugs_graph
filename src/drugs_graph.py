from conf import settings as s
import utils as ut


# reading and dataprep

df_ct = ut.get_df(s.clinical_trials_file, {'index_col': 0})
df_dr = ut.get_df(s.drugs_file, {'index_col': 0})
df_pub = ut.get_df(s.pubmed_file, {'index_col': 0})

df_ct = ut.check_for_matching_if_nan(df_ct, s.cols_ref_ct)
