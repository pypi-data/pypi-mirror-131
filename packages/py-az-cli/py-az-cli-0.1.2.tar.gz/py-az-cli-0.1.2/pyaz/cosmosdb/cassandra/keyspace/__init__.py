from .... pyaz_utils import call_az
from . import throughput


def create(account_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Create an Cassandra keyspace under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace create", locals())


def exists(account_name, name, resource_group):
    return call_az("az cosmosdb cassandra keyspace exists", locals())


def list(account_name, resource_group):
    '''
    List the Cassandra keyspaces under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace list", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a Cassandra keyspace under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace show", locals())


def delete(account_name, name, resource_group, yes=None):
    '''
    Delete the Cassandra keyspace under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace delete", locals())

