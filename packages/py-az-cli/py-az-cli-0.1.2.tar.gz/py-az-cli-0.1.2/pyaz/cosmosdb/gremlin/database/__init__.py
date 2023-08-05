from .... pyaz_utils import call_az
from . import throughput


def create(account_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Create an Gremlin database under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb gremlin database create", locals())


def exists(account_name, name, resource_group):
    return call_az("az cosmosdb gremlin database exists", locals())


def list(account_name, resource_group):
    '''
    List the Gremlin databases under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb gremlin database list", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a Gremlin database under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb gremlin database show", locals())


def delete(account_name, name, resource_group, yes=None):
    '''
    Delete the Gremlin database under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb gremlin database delete", locals())

