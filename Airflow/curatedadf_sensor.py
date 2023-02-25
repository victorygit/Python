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
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.exceptions import AirflowFailException
from airflow.models import Variable


# Default arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 2, 18,7,0,0,tzinfo=timezone('EST')),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

# Create the DAG
dag = DAG(
    'curated_pipelines_sensor',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

begin = EmptyOperator(task_id="begin", dag=dag)
end = EmptyOperator(task_id="end",trigger_rule=TriggerRule.ALL_DONE,dag=dag)
# Define a function to run the pipeline

def run_pipeline1(**kwargs):
    # Create the client
    #credentials = ServicePrincipalCredentials(
    #    client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
    #    secret='',
    #    tenant='962f21cf-93ea-449f-99bf-402e2b2987b2',
    #)
    credentials = ClientSecretCredential(
        client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
        client_secret = Variable.get("Client_Secret"),
        tenant_id='962f21cf-93ea-449f-99bf-402e2b2987b2',
    )

    client = DataFactoryManagementClient(credentials, 'a4019287-f428-40ff-8fb5-3224e84aeb1e')
   
    # Run the pipeline
    pipeline_name = kwargs['Pipelinename']
    run_response = client.pipelines.create_run(
    'oceanis-rg-dld-sb',
    'oceanis-adf-dldtest-sb',
    pipeline_name,
    None,
    None,
    None,
    None,
    {"Waitime":kwargs['waittime'],"Job":kwargs['job']}
    )
    run_id = run_response.run_id

    # Print the run ID
    print(f'Pipeline run ID: {run_id}') 
    while client.pipeline_runs.get('oceanis-rg-dld-sb', 'oceanis-adf-dldtest-sb', run_response.run_id).status in ('InProgress', 'Queued'):
        time.sleep(20) 
    if client.pipeline_runs.get('oceanis-rg-dld-sb', 'oceanis-adf-dldtest-sb', run_response.run_id).status in ('Failed'):
        raise AirflowFailException("Pipeline failed")
    
  
run_pipeline_operator1 = PythonOperator(
     task_id='run_pipeline1',
     python_callable=run_pipeline1,
     provide_context=True,
     op_kwargs={"Pipelinename":"PL_Curated_Job","waittime":"15","job":"100"},
     dag=dag,
 )

sensing_Task1 = ExternalTaskSensor(
    task_id='wait_for_pipeline1',
    dag=dag,
# exe cution_delta=timedelta(hours=-l),                         
    execution_date_fn=lambda dt: dt  - timedelta(hours=0),
    external_dag_id='run_pipeline12', 
    external_task_id='run_pipeline1')

sensing_Task2 = ExternalTaskSensor(
    task_id='wait_for_pipeline3',
    dag=dag,
# exe cution_delta=timedelta(hours=-l),                         
    execution_date_fn=lambda dt: dt  - timedelta(hours=0),
    external_dag_id='run_pipeline3', 
    external_task_id='run_pipeline3')


sleep = BashOperator(task_id='sleep',
                     bash_command='sleep 5',
                     dag=dag)


                  
# Set the dependencies
begin >> sensing_Task1  >> run_pipeline_operator1 >> end
begin >> sensing_Task2 >> run_pipeline_operator1 >> end
