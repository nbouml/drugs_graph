from dotenv import load_dotenv
import os

from pathlib import Path

import logging
from set_logging import setup_logger

logfile = "drugs_graph.log"

log = 'settings'
setup_logger('settings', logfile, logging.DEBUG)
log = logging.getLogger(log)

load_dotenv("drugs_graph/conf/.env", override=True)

title_str = Path(os.getenv('DRUGS_GRAPH_DAG_TITLE_STR', ''))
drug_str = Path(os.getenv('DRUGS_GRAPH_DAG_DRUG_STR', ''))
journal_str = Path(os.getenv('DRUGS_GRAPH_DAG_JOURNAL_STR', ''))
pubmed_str = Path(os.getenv('DRUGS_GRAPH_DAG_PUBMED_STR', ''))
date_str = Path(os.getenv('DRUGS_GRAPH_DAG_DATE_STR', ''))

input_data_path = Path(os.getenv('DRUGS_GRAPH_INPUT_DATA_PATH', ''))

clinical_trials_file = input_data_path / os.getenv('DRUGS_GRAPH_CLINICAL_TRIALS_FILE', '')
drugs_file = input_data_path / os.getenv('DRUGS_GRAPH_DRUGS_FILE', '')
pubmed_file = input_data_path / os.getenv('DRUGS_GRAPH_PUBMED_FILE', '')

cols_ref_ct = tuple(os.getenv('DRUGS_GRAPH_COLS_REF_CT', '').split(','))

output_file = input_data_path / os.getenv('DRUGS_GRAPH_OUTPUT_FILE', '')
