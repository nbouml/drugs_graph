from dotenv import load_dotenv
import os

from pathlib import Path

import logging
from drugs_graph.set_logging import setup_logger

logfile = "drugs_graph.log"

log = 'settings'
setup_logger('settings', logfile, logging.DEBUG)
log = logging.getLogger(log)

load_dotenv("drugs_graph/conf/.env", override=True)

title_str = os.getenv('DRUGS_GRAPH_DAG_TITLE_STR', '')
drug_str = os.getenv('DRUGS_GRAPH_DAG_DRUG_STR', '')
journal_str = os.getenv('DRUGS_GRAPH_DAG_JOURNAL_STR', '')
pubmed_str = os.getenv('DRUGS_GRAPH_DAG_PUBMED_STR', '')
date_str = os.getenv('DRUGS_GRAPH_DAG_DATE_STR', '')
scientific_title_str = os.getenv('DRUGS_GRAPH_DAG_SCIENTIFIC_TITLE', '')
clinical_trials_str = os.getenv('DRUGS_GRAPH_DAG_CLINICAL_TRIALS_STR', '')

input_data_path = Path(os.getenv('DRUGS_GRAPH_INPUT_DATA_PATH', ''))
input_base_path = Path(os.getenv('DRUGS_GRAPH_BASE_PATH', ''))
input_results_path = Path(os.getenv('DRUGS_GRAPH_RESULTS_PATH', '')) / os.getenv('DRUGS_GRAPH_OUTPUT_FILE', '')
results_path = Path(os.getenv('DRUGS_GRAPH_RESULTS_PATH', ''))

clinical_trials_file = os.getenv('DRUGS_GRAPH_CLINICAL_TRIALS_FILE', '')
drugs_file = os.getenv('DRUGS_GRAPH_DRUGS_FILE', '')
pubmed_file = os.getenv('DRUGS_GRAPH_PUBMED_FILE', '')
journals_file = os.getenv('DRUGS_GRAPH_JOURNALS_FILE', '')
output_file = os.getenv('DRUGS_GRAPH_OUTPUT_FILE', '')

cols_ref_ct = tuple(os.getenv('DRUGS_GRAPH_COLS_REF_CT', '').split(','))

engine_type = os.getenv('DRUGS_GRAPH_ENGINE', '')

if not input_base_path.is_dir():
    os.mkdir(input_base_path)

if not results_path.is_dir():
    os.mkdir(results_path)
