from datetime import datetime, timedelta

from airflow.models import DAG, BaseOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
from airflow.providers.microsoft.azure.sensors.data_factory import AzureDataFactoryPipelineRunStatusSensor
from airflow.utils.edgemodifier import Label

with DAG(
    dag_id="adf_pipeline_with_Sensor",
    start_date=datetime(2021, 8, 13),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
        "azure_data_factory_conn_id": "azure_data_factory_sb",
        #"factory_name": "my-data-factory",  # This can also be specified in the ADF connection.
        #"resource_group_name": "my-resource-group",  # This can also be specified in the ADF connection.
    },
    default_view="graph",
) as dag:
    begin = EmptyOperator(task_id="begin")
    end1 = EmptyOperator(task_id="end2")
    end2 = EmptyOperator(task_id="end2")

    # [START howto_operator_adf_run_pipeline]
    run_pipeline1: BaseOperator = AzureDataFactoryRunPipelineOperator(
        task_id="run_pipeline1",
        pipeline_name="PL_Job3",
        parameters={"Waitime":"21","Job":"300"},
    )
    # [END howto_operator_adf_run_pipeline]

 
    pipeline_run_sensor1: BaseOperator = AzureDataFactoryPipelineRunStatusSensor(
        task_id="pipeline_run_sensor1",
        run_id=run_pipeline1.output["run_id"],
    )
    # [END howto_operator_adf_run_pipeline_async]

    begin >> Label("No async wait") >> run_pipeline1 >> end1
    begin >> Label("No async wait") >> pipeline_run_sensor1 >> end2