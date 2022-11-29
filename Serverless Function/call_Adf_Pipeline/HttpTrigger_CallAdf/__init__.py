import logging

import azure.functions as func

from azure.identity import ClientSecretCredential 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta
import time

def print_item(group):
    """Print an Azure object instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    if hasattr(group, 'location'):
        print("\tLocation: {}".format(group.location))
    if hasattr(group, 'tags'):
        print("\tTags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)

def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")

def print_activity_run_details(activity_run):
    """Print activity run details."""
    print("\n\tActivity run details\n")
    print("\tActivity run status: {}".format(activity_run.status))
    #if activity_run.status == 'Succeeded':
        #print("\tNumber of bytes read: {}".format(activity_run.output['dataRead']))
        #print("\tNumber of bytes written: {}".format(activity_run.output['dataWritten']))
        #print("\tCopy duration: {}".format(activity_run.output['copyDuration']))
    #else:
        #print("\tErrors: {}".format(activity_run.error['message']))


def run_pipeline():

    # Azure subscription ID
    subscription_id = 'a4019287-f428-40ff-8fb5-3224e84aeb1e'

    # This program creates this resource group. If it's an existing resource group, comment out the code that creates the resource group
    rg_name = 'oceanis-rg-dld-sb'

    # The data factory name. It must be globally unique.
    df_name = 'oceanis-adf-dld-sb'

    # Specify your Active Directory client ID, client secret, and tenant ID
    credentials = ClientSecretCredential(client_id='02ad2a23-9147-4e47-a0d6-b079c55a636c', client_secret='n_C8Q~GuwTLGOsR8Rtqe_ibugirX~BER5W2uUaKI', tenant_id='962f21cf-93ea-449f-99bf-402e2b2987b2') 

    # Specify following for Soverign Clouds, import right cloud constant and then use it to connect.
    # from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD as CLOUD
    # credentials = DefaultAzureCredential(authority=CLOUD.endpoints.active_directory, tenant_id=tenant_id)

    resource_client = ResourceManagementClient(credentials, subscription_id)
    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    # Create a pipeline run
    #p_name = 'pipeline_wait'    
    #run_response = adf_client.pipelines.create_run(rg_name, df_name, p_name, parameters={})
    p_name = 'PL_CallTest'
    run_response = adf_client.pipelines.create_run(rg_name, df_name, p_name, parameters={"Waittime":10,"TableName":"PY"})
    # Monitor the pipeline run
    #time.sleep(30)
    #pipeline_run = adf_client.pipeline_runs.get(
    #    rg_name, df_name, run_response.run_id)
    #print("\n\tPipeline run status: {}".format(pipeline_run.status))
    #filter_params = RunFilterParameters(
    #    last_updated_after=datetime.now() - timedelta(1), last_updated_before=datetime.now() + timedelta(1))
    #query_response = adf_client.activity_runs.query_by_pipeline_run(
    #    rg_name, df_name, pipeline_run.run_id, filter_params)
    #print_activity_run_details(query_response.value[0])



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        run_pipeline()
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully after pipeline run.")
        
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
