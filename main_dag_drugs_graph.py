import pendulum

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

from drugs_graph.conf import settings as s
import logging
from drugs_graph.set_logging import setup_logger

from drugs_graph.src.engines import get_engine
import main_drugs_graph as mdg


logfile = "drugs_graph.log"

log = 'main'
setup_logger(log, logfile, logging.DEBUG)
log = logging.getLogger(log)

engine = get_engine()
input_data_path = s.input_data_path
base_path = s.input_base_path


# step 1
def data_prep():
    mdg.data_prep_clin_t()
    mdg.data_prep_pubmed()
    mdg.data_prep_drug()


# step 2
def get_journals_df():
    mdg.build_journals_df()
    mdg.group_by_for_df_journals()


with DAG(
    dag_id="Drugs_graph",
    schedule_interval="@once",
    start_date=pendulum.datetime(2022, 10, 25, tz="UTC")
) as dag:

    data_prep = PythonOperator(
        task_id='data_prep',
        python_callable=data_prep,
    )

    get_journals_cleand = PythonOperator(
        task_id='journals',
        python_callable=get_journals_df,
    )

    final_results = PythonOperator(
        task_id='final_results',
        python_callable=mdg.final_result,
    )

    cleaning = PythonOperator(
        task_id='cleaning',
        python_callable=mdg.cleaning,
    )

    data_prep >> get_journals_cleand >> final_results >> cleaning
