from dotenv import load_dotenv
import os

load_dotenv("drugs_graph/conf/.env", override=True)

input_data_path = os.getenv('DRUGS_GRAPH_INPUT_DATA_PATH', '')

clinical_trials_file = os.getenv('DRUGS_GRAPH_CLINICAL_TRIALS_FILE', '')
drugs_file = os.getenv('DRUGS_GRAPH_DRUGS_FILE', '')
pubmed_file = os.getenv('DRUGS_GRAPH_PUBMED_FILE', '')

output_file = os.getenv('DRUGS_GRAPH_OUTPUT_FILE', '')
