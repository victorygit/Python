from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow import DAG
import time
import json
from pytz import timezone


# Default arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 2,23,5,0,0,tzinfo=timezone('EST')),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

# Create the DAG
dag = DAG(
    'followingjob',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)
#	Define the sensor for sensing the completion of DAG_B.Task_B
sensing_Task = ExternalTaskSensor(
    task_id='wait_for_dependentJob',
    dag=dag,
# exe cution_delta=timedelta(hours=-l),                         
    execution_date_fn=lambda dt: dt  - timedelta(hours=0),
    external_dag_id='dependjob', 
    external_task_id='task_sleep1')
#	Set the upstream dependency for Task_A
task_sleep = BashOperator(task_id='task_sleep2',
                     bash_command='sleep 5',
                     dag=dag)

task_sleep >> sensing_Task

