import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import config

# ----------------------------------------------------------------------------------------------------------
# Prerequistes -
#
# 1. An Azure Cosmos account -
#    https://docs.microsoft.com/azure/cosmos-db/create-cosmosdb-resources-portal#create-an-azure-cosmos-db-account
#
# 2. Microsoft Azure Cosmos PyPi package -
#    https://pypi.python.org/pypi/azure-cosmos/
# ----------------------------------------------------------------------------------------------------------
# Sample - demonstrates the basic CRUD operations on a Item resource for Azure Cosmos
# ----------------------------------------------------------------------------------------------------------

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

def create_items(container):
    print('\nCreating Items\n')

    # Create a SalesOrder object. This object has nested properties and various types including numbers, DateTimes and strings.
    # This can be saved as JSON as is without converting into rows/columns.
    sales_order = get_sales_order("SalesOrder1")
    container.create_item(body=sales_order)

    # As your app evolves, let's say your object has a new schema. You can insert SalesOrderV2 objects without any
    # changes to the database tier.
    sales_order2 = get_sales_order_v2("SalesOrder2")
    container.create_item(body=sales_order2)

def scale_container(container):
    print('\nScaling Container\n')
    
    # You can scale the throughput (RU/s) of your container up and down to meet the needs of the workload. Learn more: https://aka.ms/cosmos-request-units
    try:
        offer = container.read_offer()
        print('Found Offer and its throughput is \'{0}\''.format(offer.offer_throughput))

        offer.offer_throughput += 100
        container.replace_throughput(offer.offer_throughput)

        print('Replaced Offer. Offer Throughput is now \'{0}\''.format(offer.offer_throughput))
    
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code == 400:
            print('Cannot read container throuthput.');
            print(e.http_error_message);
        else:
            raise;

def read_item(container, doc_id, account_number):
    print('\nReading Item by Id\n')

    # We can do an efficient point read lookup on partition key and id
    response = container.read_item(item=doc_id, partition_key=account_number)

    print('Item read by Id {0}'.format(doc_id))
    print('Partition Key: {0}'.format(response.get('partitionKey')))
    print('Subtotal: {0}'.format(response.get('subtotal')))

def read_items(container):
    print('\nReading all items in a container\n')

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('Item Id: {0}'.format(doc.get('id')), 'EmployeeId: {0}'.format(doc.get('EmployeeId')))

def query_all_items(container):
    print('\nQuerying for an  Item cross Partition Key\n')

    # Including the partition key value of account_number in the WHERE filter results in a more efficient query
    items = list(container.query_items(
        query="SELECT * FROM r ",enable_cross_partition_query=True
    ))
    for item in items:
        print (item)

def query_items(container, country):
    print('\nQuerying for an  Item by Country partition\n')
    print('partition valie',country)
    # Including the partition key value of account_number in the WHERE afilter results in a more efficient query
    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.country=@country_value",
        parameters=[
            { "name":"@country_value", "value": country }
        ]
    ))

    for item in items:
        print (item)

def replace_item(container, doc_id, account_number):
    print('\nReplace an Item\n')

    read_item = container.read_item(item=doc_id, partition_key=account_number)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.replace_item(item=read_item, body=read_item)

    print('Replaced Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['subtotal']))

def upsert_item(container, doc_id, account_number):
    print('\nUpserting an item\n')

    read_item = container.read_item(item=doc_id, partition_key=account_number)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.upsert_item(body=read_item)

    print('Upserted Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['subtotal']))

def delete_item(container, doc_id, account_number):
    print('\nDeleting Item by Id\n')

    response = container.delete_item(item=doc_id, partition_key=account_number)

    print('Deleted item\'s Id is {0}'.format(doc_id))



def run_sample():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    try:
        # setup database for this sample
        try:
            db = client.create_database(id=DATABASE_ID)
            print('Database with id \'{0}\' created'.format(DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))

        # setup container for this sample
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/partitionKey'))
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

        read_items(container)
        query_all_items(container)
        query_items(container, 'CA')
  

        # cleanup database after sample
        #try:
        #    client.delete_database(db)

        #except exceptions.CosmosResourceNotFoundError:
        #    pass

    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

    finally:
            print("\nrun_sample done")

if __name__ == '__main__':
    run_sample()
