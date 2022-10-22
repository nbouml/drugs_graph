from dotenv import load_dotenv
import os
import logging as log

from pathlib import Path

log.basicConfig(filename="logs",
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=log.DEBUG)

load_dotenv("drugs_graph/conf/.env", override=True)

input_data_path = Path(os.getenv('DRUGS_GRAPH_INPUT_DATA_PATH', ''))

clinical_trials_file = Path(os.getenv('DRUGS_GRAPH_CLINICAL_TRIALS_FILE', ''))
drugs_file = Path(os.getenv('DRUGS_GRAPH_DRUGS_FILE', ''))
pubmed_file = Path(os.getenv('DRUGS_GRAPH_PUBMED_FILE', ''))

output_file = Path(os.getenv('DRUGS_GRAPH_OUTPUT_FILE', ''))
