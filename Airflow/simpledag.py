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
    'simpledag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

begin = EmptyOperator(task_id="begin", dag=dag)
end = EmptyOperator(task_id="end",trigger_rule=TriggerRule.ALL_DONE,dag=dag)
# Define a function to run the pipeline



sleep = BashOperator(task_id='sleep',
                     bash_command='sleep 5',
                     dag=dag)
# Set the dependencies
begin >> sleep >> end
