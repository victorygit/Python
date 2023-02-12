from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 2, 11),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

# Create the DAG
dag = DAG(
    'run_azure_data_factory_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

# Define a function to run the pipeline

def run_pipeline1(**kwargs):
    # Create the client
    #credentials = ServicePrincipalCredentials(
    #    client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
    #    secret='QCK8Q~zLvTGRySRM6UtfafiVcyBvo6CmTSkBXcpk',
    #    tenant='962f21cf-93ea-449f-99bf-402e2b2987b2',
    #)
    credentials = ClientSecretCredential(
        client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
        client_secret='QCK8Q~zLvTGRySRM6UtfafiVcyBvo6CmTSkBXcpk',
        tenant_id='962f21cf-93ea-449f-99bf-402e2b2987b2',
    )
    
    client = DataFactoryManagementClient(credentials, 'a4019287-f428-40ff-8fb5-3224e84aeb1e')
    #client = ResourceManagementClient(credentials, 'a4019287-f428-40ff-8fb5-3224e84aeb1e')

    # Run the pipeline
    pipeline_name = 'PL_Job1'
    run_response = client.ppipelines.create_run(
    'oceanis-rg-dld-sb',
    'oceanis-adf-dldtest-sb',
    pipeline_name,
    )
    run_id = run_response.run_id

    # Print the run ID
    print(f'Pipeline run ID: {run_id}')

def run_pipeline2(**kwargs):
    # Create the client
    credentials = ServicePrincipalCredentials(
        client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
        secret='QCK8Q~zLvTGRySRM6UtfafiVcyBvo6CmTSkBXcpk',
        tenant='962f21cf-93ea-449f-99bf-402e2b2987b2',
    )
    client = DataFactoryManagementClient(credentials, 'a4019287-f428-40ff-8fb5-3224e84aeb1e')

    # Run the pipeline
    pipeline_name = 'PL_Job2'
    run_response = client.pipelines.create_run(
    'oceanis-rg-dld-sb',
    'oceanis-adf-dldtest-sb',
    pipeline_name,
    )
    run_id = run_response.run_id

    # Print the run ID
    print(f'Pipeline run ID: {run_id}')
# Create a PythonOperator to run the pipeline
run_pipeline_operator1 = PythonOperator(
     task_id='run_pipeline1',
     python_callable=run_pipeline1,
     provide_context=True,
     dag=dag,
 )
run_pipeline_operator2 = PythonOperator(
     task_id='run_pipeline2',
     python_callable=run_pipeline2,
     provide_context=True,
     dag=dag,
 )
sleep = BashOperator(task_id='sleep',
                     bash_command='sleep 5',
                     dag=dag)
# Set the dependencies
sleep >> run_pipeline_operator1 >> run_pipeline_operator2