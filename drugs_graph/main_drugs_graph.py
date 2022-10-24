from conf import settings as s
from src import utils as ut
import logging
from set_logging import setup_logger

logfile = "drugs_graph.log"

log = 'main'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)


# reading and dataprep

log.info('Start')

df_ct = ut.get_df(s.clinical_trials_file, {'index_col': 0})
df_dr = ut.get_df(s.drugs_file, {'index_col': 0})
df_pub = ut.get_df(s.pubmed_file, {'index_col': 0})

df_ct = ut.check_for_matching_if_nan(df_ct, s.cols_ref_ct)

drug_names = df_dr['drug'].to_list()
