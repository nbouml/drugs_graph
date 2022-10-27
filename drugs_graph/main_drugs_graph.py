import pandas as pd
import json

from conf import settings as s
from src import utils as ut
import logging
from drugs_graph.set_logging import setup_logger


logfile = "drugs_graph.log"

log = 'main'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)

# reading and dataprep

log.info('Start')


# step 1
def data_prep(input_data_path=s.input_data_path, base_path=s.input_base_path):
    df_ct_in = ut.get_df(input_data_path / s.clinical_trials_file, {'index_col': 0})
    df_dr_in = ut.get_df(input_data_path / s.drugs_file, {'index_col': 0})
    df_pub_in = ut.get_df(input_data_path / s.pubmed_file, {'index_col': 0})

    df_ct_in = ut.check_for_matching_if_nan(df_ct_in, s.cols_ref_ct)
    df_pub_in = ut.convert_col_in_datetime(df_pub_in, ('date', ), day_first=True)
    df_ct_in = ut.convert_col_in_datetime(df_ct_in, ('date', ), day_first=True)

    # TODO: save method
    df_ct_in.to_csv(base_path / s.clinical_trials_file)
    df_dr_in.to_csv(base_path / s.drugs_file)
    df_pub_in.to_csv(base_path / s.pubmed_file)


# step 2
def get_journals_df(input_base_path=s.input_base_path):
    df_pub = ut.get_df(input_base_path / s.pubmed_file, {'index_col': 0})
    df_ct = ut.get_df(input_base_path / s.clinical_trials_file, {'index_col': 0})

    df_pub = ut.convert_col_in_datetime(df_pub, ('date', ), day_first=True)
    df_ct = ut.convert_col_in_datetime(df_ct, ('date', ), day_first=True)

    df_journals_pub = df_pub[[s.journal_str, s.date_str]].copy()
    df_journals_pub.set_index(s.journal_str, inplace=True)
    df_journals_ct = df_ct[[s.journal_str, s.date_str]].copy()
    df_journals_ct.set_index(s.journal_str, inplace=True)
    df_journals_concat = pd.concat([df_journals_pub, df_journals_ct])
    df_journals_concat = df_journals_concat.date.apply(lambda x: x.strftime('%d-%m-%Y'))
    df_journals = df_journals_concat.groupby(s.journal_str).transform(lambda x: ','.join(x))

    df_journals.to_csv(input_base_path / s.journals_file)


def do_final_result(input_base_path=s.input_base_path):
    df_pub = ut.get_df(input_base_path / s.pubmed_file, {'index_col': 0})
    df_ct = ut.get_df(input_base_path / s.clinical_trials_file, {'index_col': 0})
    df_journ = ut.get_df(input_base_path / s.journals_file, {'index_col': 0})
    df_drug = ut.get_df(input_base_path / s.drugs_file, {'index_col': 0})

    drug_names = df_drug.drug.to_list()
    res = {}
    # step 3
    for drug in drug_names:
        res[drug] = {s.pubmed_str: ut.get_sub_target_dict(df_pub, drug, s.title_str, s.date_str),
                     s.clinical_trials_str: ut.get_sub_target_dict(df_ct, drug, s.scientific_title_str, s.date_str),
                     s.journal_str: df_journ.to_dict()}

    with open(s.results_path / s.output_file, 'w') as f:
        json.dump(res, f)


log.info('data prep')
data_prep()

log.info('getting info from journal table')
get_journals_df()

log.info('Graph construction')
do_final_result()
