from dotenv import load_dotenv
import os

from pathlib import Path

import logging
from set_logging import setup_logger

setup_logger('log', 'drugs_graph.log', logging.DEBUG)
log = logging.getLogger(__name__)

load_dotenv("conf/.env", override=True)

input_data_path = Path(os.getenv('DRUGS_GRAPH_INPUT_DATA_PATH', ''))

clinical_trials_file = input_data_path / os.getenv('DRUGS_GRAPH_CLINICAL_TRIALS_FILE', '')
drugs_file = input_data_path / os.getenv('DRUGS_GRAPH_DRUGS_FILE', '')
pubmed_file = input_data_path / os.getenv('DRUGS_GRAPH_PUBMED_FILE', '')

cols_ref_ct = tuple(os.getenv('DRUGS_GRAPH_COLS_REF_CT', '').split(','))

output_file = input_data_path / os.getenv('DRUGS_GRAPH_OUTPUT_FILE', '')
