from .... pyaz_utils import call_az
from . import throughput


def create(account_name, database_name, name, partition_key_path, resource_group, analytical_storage_ttl=None, conflict_resolution_policy=None, idx=None, max_throughput=None, partition_key_version=None, throughput=None, ttl=None, unique_key_policy=None):
    '''
    Create an SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container create", locals())


def update(account_name, database_name, name, resource_group, analytical_storage_ttl=None, idx=None, ttl=None):
    '''
    Update an SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container update", locals())


def exists(account_name, database_name, name, resource_group):
    return call_az("az cosmosdb sql container exists", locals())


def list(account_name, database_name, resource_group):
    '''
    List the SQL containers under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container list", locals())


def show(account_name, database_name, name, resource_group):
    '''
    Show the details of a SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container show", locals())


def delete(account_name, database_name, name, resource_group, yes=None):
    '''
    Delete the SQL container under an Azure Cosmos DB SQL database.
    '''
    return call_az("az cosmosdb sql container delete", locals())

