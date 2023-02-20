from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from datetime import datetime

default_args = {
    'start_date': datetime(2021, 1, 1)
}

def _downloading():
    print('downloading')

with DAG('trigger_dag', 
    schedule_interval=timedelta(days=1), 
    default_args=default_args, 
    catchup=False) as dag:

    downloading = PythonOperator(
        task_id='downloading',
        python_callable=_downloading
    )