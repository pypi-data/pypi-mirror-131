from ..... pyaz_utils import _call_az

def show(account_name, database_name, name, resource_group):
    '''
    Get the throughput of the MongoDB collection under an Azure Cosmos DB MongoDB database.
    '''
    return _call_az("az cosmosdb mongodb collection throughput show", locals())


def update(account_name, database_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Update the throughput of the MongoDB collection under an Azure Cosmos DB MongoDB database.
    '''
    return _call_az("az cosmosdb mongodb collection throughput update", locals())


def migrate(account_name, database_name, name, resource_group, throughput_type):
    '''
    Migrate the throughput of the MongoDB collection between autoscale and manually provisioned.
    '''
    return _call_az("az cosmosdb mongodb collection throughput migrate", locals())

