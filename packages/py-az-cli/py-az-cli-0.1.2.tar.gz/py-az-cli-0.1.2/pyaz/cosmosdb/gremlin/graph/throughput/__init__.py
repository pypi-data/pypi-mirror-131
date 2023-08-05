from ..... pyaz_utils import call_az

def show(account_name, database_name, name, resource_group):
    '''
    Get the throughput of the Gremlin graph under an Azure Cosmos DB Gremlin database.
    '''
    return call_az("az cosmosdb gremlin graph throughput show", locals())


def update(account_name, database_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Update the throughput of the Gremlin graph under an Azure Cosmos DB Gremlin database.
    '''
    return call_az("az cosmosdb gremlin graph throughput update", locals())


def migrate(account_name, database_name, name, resource_group, throughput_type):
    '''
    Migrate the throughput of the Gremlin Graph between autoscale and manually provisioned.
    '''
    return call_az("az cosmosdb gremlin graph throughput migrate", locals())

