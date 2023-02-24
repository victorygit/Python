from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.datafactory import DataFactoryManagementClient
from datetime import datetime, timedelta
from airflow.models import Variable

# Default arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'run_azure_data_factory_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

# Define a function to run the pipeline

def run_pipeline(**kwargs):
    # Create the client
    credentials = ServicePrincipalCredentials(
        client_id='12c29c27-283d-46c8-9b3a-1515836cf62a',
        client_secret = Variable.get("Client_Secret"),
        tenant_id='962f21cf-93ea-449f-99bf-402e2b2987b2',
    )
    client = DataFactoryManagementClient(credentials, 'your_subscription_id')

 # Run the pipeline
    pipeline_name = 'PL_Job1'
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

 # Create a PythonOperator to run the pipeline
run_pipeline_operator = PythonOperator(
     task_id='run_pipeline',
     python_callable=run_pipeline,
     provide_context=True,
     dag=dag,
 )

 # Set the dependencies
run_pipeline_operator