import json
import os

from drugs_graph.conf import settings as s
from drugs_graph.src import utils as ut
import logging
from drugs_graph.set_logging import setup_logger

from drugs_graph.src.engines import get_engine


logfile = "drugs_graph.log"

log = 'main'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)

engine = get_engine()
input_data_path = s.input_data_path
base_path = s.input_base_path


def data_prep_clin_t():
    """
    data preparation for clinical trials tile

    Returns
    -------
    None

    """
    def rename_col(df, dict_rename):
        return df.rename(columns=dict_rename)
    fp_in = input_data_path / s.clinical_trials_file
    clin_t_v1 = engine.submit(ut.check_for_matching_if_nan,
                              fp_in,
                              base_path / s.clinical_trials_file,
                              kwargs_opera={'ref_cols': s.cols_ref_ct})

    clin_t_v2 = engine.submit(ut.convert_col_in_datetime,
                              clin_t_v1.result(),
                              base_path / s.clinical_trials_file,
                              kwargs_opera={'columns': ('date',), 'day_first': True})

    engine.submit(rename_col,
                  clin_t_v2.result(),
                  base_path / s.clinical_trials_file,
                  kwargs_opera={'dict_rename': {s.scientific_title_str: s.title_str}}
                  )


def data_prep_pubmed():
    """
    data preparation for PubMed file

    Returns
    -------
    None

    """
    fp_in = input_data_path / s.pubmed_file
    f_out = base_path / s.pubmed_file

    engine.submit(ut.convert_col_in_datetime,
                  fp_in,
                  f_out,
                  kwargs_opera={'columns': ('date',), 'day_first': True})


def data_prep_drug():
    """
    data preparation for drugs file

    Returns
    -------
    None

    """
    file_name = s.drugs_file

    fp_in = input_data_path / file_name
    f_out = base_path / file_name

    engine.submit(lambda x: x,
                  fp_in,
                  f_out)


def build_journals_df():
    """
    Construction of journals table.

    Returns
    -------
    None

    """
    file_name = s.journals_file
    files_path = (base_path / s.pubmed_file, base_path / s.clinical_trials_file)

    f_out = base_path / file_name

    cols_comm = (s.journal_str, s.date_str, s.title_str)
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
    None

    """
    def my_gb(df_in):
        df_in = df_in.reset_index()
        df_in = df_in.drop_duplicates([s.journal_str, s.date_str])
        df_in = df_in.set_index(s.journal_str)
        df_in = df_in.groupby(s.journal_str).transform(lambda x: ','.join(x))
        return df_in

    f_out = base_path / s.journals_file

    engine.submit(my_gb,
                  f_out,
                  f_out)


def final_result():
    """
    Build and save the final result.

    Returns
    -------
    None

    """
    def do_result(df_ct, df_journ, df_drug, df_pub):
        drug_names = df_drug.drug.to_list()
        res = {}
        for drug in drug_names:
            df_journ_drug = df_journ.copy()
            df_journ_drug.reset_index(inplace=True)
            idx_drug_journ = ut.str_sniffer(drug, df_journ_drug, s.title_str)
            df_journ_drug = df_journ_drug.loc[idx_drug_journ].set_index(s.journal_str)
            res[drug] = {s.pubmed_str: ut.get_sub_target_dict(df_pub, drug, s.title_str, s.date_str),
                         s.clinical_trials_str: ut.get_sub_target_dict(df_ct, drug, s.title_str, s.date_str),
                         s.journal_str: df_journ_drug[s.date_str].to_dict()}

        with open(s.results_path / s.output_file, 'w') as f:
            json.dump(res, f)

    files = [s.clinical_trials_file, s.journals_file, s.drugs_file, s.pubmed_file]
    files_path = tuple([base_path / i for i in files])

    engine.submit(do_result,
                  files_path,
                  None)


def cleaning():
    """
    Clean temporary files

    Returns
    -------
    None

    """
    def del_files(_dummy, path):
        for file_name in os.listdir(path):
            file = path / file_name
            if os.path.isfile(file):
                log.info(f'Deleting file: {str(file)}')
                os.remove(file)

    engine.submit(del_files,
                  base_path,
                  kwargs_opera={'path': base_path})


if __name__ == "__main__":
    log.info('Start')
    # step 1
    data_prep_clin_t()
    data_prep_pubmed()
    data_prep_drug()

    # step 2
    build_journals_df()
    group_by_for_df_journals()

    # step 3
    final_result()

    # step 4
    cleaning()

    log.info('end')
