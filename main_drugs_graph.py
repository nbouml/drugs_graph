import json

from drugs_graph.conf import settings as s
from drugs_graph.src import utils as ut
import logging
from drugs_graph.set_logging import setup_logger

from drugs_graph.src.engines import get_engine


logfile = "drugs_graph.log"

log = 'main'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)

# reading and dataprep

log.info('Start')

engine = get_engine()
input_data_path = s.input_data_path
base_path = s.input_base_path


def data_prep_clin_t():
    fp_in = input_data_path / s.clinical_trials_file
    engine.submit(ut.check_for_matching_if_nan,
                  fp_in,
                  base_path / s.clinical_trials_file,
                  kwargs_opera={'ref_cols': s.cols_ref_ct})

    engine.submit(ut.convert_col_in_datetime,
                  base_path / s.clinical_trials_file,
                  base_path / s.clinical_trials_file,
                  kwargs_opera={'columns': ('date',), 'day_first': True})


def data_prep_pubmed():
    fp_in = input_data_path / s.pubmed_file
    f_out = base_path / s.pubmed_file

    engine.submit(ut.convert_col_in_datetime,
                  fp_in,
                  f_out,
                  kwargs_opera={'columns': ('date',), 'day_first': True})


def data_prep_drug():
    file_name = s.drugs_file

    fp_in = input_data_path / file_name
    f_out = base_path / file_name

    engine.submit(lambda x: x,
                  fp_in,
                  f_out)


def build_journals_df():
    file_name = s.journals_file
    files_path = (base_path / s.pubmed_file, base_path / s.clinical_trials_file)

    f_out = base_path / file_name

    cols_comm = (s.journal_str, s.date_str)
    engine.submit(ut.concat_cols_from_dfs,
                  files_path,
                  f_out,
                  kwargs_opera={"cols_comm": cols_comm,
                                "index_col": s.journal_str})


def group_by_for_df_journals():
    """
    group journals by dates
    Returns
    -------

    """
    def my_gb(df_in):
        df_in = df_in.groupby(s.journal_str).transform(lambda x: ','.join(x))
        return df_in

    f_out = base_path / s.journals_file

    engine.submit(my_gb,
                  f_out,
                  f_out)


def final_result():
    def do_result(df_ct, df_journ, df_drug, df_pub):
        drug_names = df_drug.drug.to_list()
        res = {}
        for drug in drug_names:
            res[drug] = {s.pubmed_str: ut.get_sub_target_dict(df_pub, drug, s.title_str, s.date_str),
                         s.clinical_trials_str: ut.get_sub_target_dict(df_ct, drug, s.scientific_title_str, s.date_str),
                         s.journal_str: df_journ.to_dict()}

        with open(s.results_path / s.output_file, 'w') as f:
            json.dump(res, f)

    files = [s.clinical_trials_file, s.journals_file, s.drugs_file, s.pubmed_file]
    files_path = tuple([base_path / i for i in files])

    # step 3
    engine.submit(do_result,
                  files_path,
                  None)


# step 1
data_prep_clin_t()
data_prep_pubmed()
data_prep_drug()

# step 2
build_journals_df()
group_by_for_df_journals()

# step 3
final_result()

log.info('end')
