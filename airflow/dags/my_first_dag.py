from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the DAG
default_args = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'my_data_pipeline_dag',
    default_args=default_args,
    description='A DAG for collecting data',
    schedule_interval=None,  # Replace with your desired schedule interval
    start_date=datetime(2024, 6, 15),
    catchup=False,
    tags=['example'],
) as dag:
    dag.doc_md = """
    This is my first DAG in airflow.
    I can write documentation in Markdown here with **bold text** or __bold text__.
    """

    # Task to collect data from REST API (file1)
    collect_data_1 = BashOperator(
        task_id='collect_data_1',
        bash_command='python "/home/wsl/airflow/dags/Collect Data/covid_19_usa.py"',  # Corrected path format and added quotes
    )
    collect_data_2 = BashOperator(
        task_id='collect_data_2',
        bash_command='python "/home/wsl/airflow/dags/Collect Data/covid_19_europe.py"',  # Corrected path format and added quotes
    )
    data_processing = BashOperator(
        task_id='data_processing',
        bash_command='python "/home/wsl/airflow/dags/Collect Data/data_processing.py"',  # Corrected path format and added quotes
    )
    index_elastic = BashOperator(
        task_id='index_elastic',
        bash_command='python "/home/wsl/airflow/dags/Collect Data/elastic_index.py"',  # Corrected path format and added quotes
    )
    collect_data_1 >> collect_data_2 >> data_processing >> index_elastic
