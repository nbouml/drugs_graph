import pandas as pd

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


def data_prep():
    global df_ct
    global df_dr
    global df_pub

    df_ct = ut.get_df(s.clinical_trials_file, {'index_col': 0})
    df_dr = ut.get_df(s.drugs_file, {'index_col': 0})
    df_pub = ut.get_df(s.pubmed_file, {'index_col': 0})


df_ct = ut.check_for_matching_if_nan(df_ct, s.cols_ref_ct)

drug_names = df_dr['drug'].to_list()

res = {}


def get_sub_target_dict(data: pd.DataFrame, str_target: str, main_col: str, date_col: str) -> dict:
    index = ut.str_sniffer(str_target, data, main_col)
    sub_df = data.loc[index, [main_col, date_col]]
    sub_df = sub_df.set_index(main_col)
    return sub_df[date_col].to_dict()


def get_journals_df():
    df_journals_pub = df_pub[[s.journal_str, s.date_str]].copy()
    df_journals_pub.set_index(s.journal_str, inplace=True)

    df_journals_ct = df_ct[[s.journal_str, s.date_str]].copy()
    df_journals_ct.set_index(s.journal_str, inplace=True)

    df_journals_concat = pd.concat([df_journals_pub, df_journals_ct])
    df_journals = df_journals_concat.groupby(s.journal_str).transform(lambda x: ','.join(x))
    return df_journals


for drug in drug_names:
    drug_pub_title_index = ut.str_sniffer(drug, df_pub, s.title_str)
    df_jour = get_journals_df()
    res[drug] = {s.pubmed_str: get_sub_target_dict(df_pub, drug, s.title_str, s.date_str),
                 s.journal_str: df_jour.to_dict()}
