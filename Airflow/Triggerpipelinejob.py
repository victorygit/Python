from airflow import DAG
import time
import json
from pytz import timezone
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.empty import EmptyOperator
from airflow.providers.microsoft.azure.sensors.data_factory import AzureDataFactoryPipelineRunStatusSensor
from airflow.exceptions import AirflowFailException
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# Default arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 2, 18,5,0,0,tzinfo=timezone('EST')),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

# Create the DAG
dag = DAG(
    'TriggerPipelineJob',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)


# Define a function to run the pipeline

trigger_target2 = TriggerDagRunOperator(
        task_id='trigger_pipeline1',
        trigger_dag_id='run_pipeline12',
        execution_date='{{ ds }}',
        reset_dag_run=False,
        wait_for_completion=True,
        dag = dag,
    )

trigger_target1 = TriggerDagRunOperator(
        task_id='trigger_pipeline3',
        trigger_dag_id='run_pipeline3',
        execution_date='{{ ds }}',
        reset_dag_run=False,
        wait_for_completion=True,
        dag = dag,
    )
trigger_target3 = TriggerDagRunOperator(
        task_id='trigger_curatedjob',
        trigger_dag_id='curated_pipelines_sensor',
        execution_date='{{ ds }}',
        reset_dag_run=False,
        wait_for_completion=True,
        dag = dag,
    )


sleep = BashOperator(task_id='sleep',
                     bash_command='sleep 5',
                     dag=dag)
# Set the dependencies
trigger_target1
trigger_target2 
trigger_target3 
