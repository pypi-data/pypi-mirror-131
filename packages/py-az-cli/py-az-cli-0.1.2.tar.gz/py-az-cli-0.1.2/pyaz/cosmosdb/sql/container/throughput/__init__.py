from ..... pyaz_utils import call_az

def show(account_name, database_name, name, resource_group):
    '''
    Get the throughput of the SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container throughput show", locals())


def update(account_name, database_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Update the throughput of the SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container throughput update", locals())


def migrate(account_name, database_name, name, resource_group, throughput_type):
    '''
    Migrate the throughput of the SQL container between autoscale and manually provisioned.
    '''
    return call_az("az cosmosdb sql container throughput migrate", locals())

