from .... pyaz_utils import call_az

def create(account_name, body, container_name, database_name, name, resource_group):
    '''
    Create an SQL user defined function under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql user-defined-function create", locals())


def update(account_name, body, container_name, database_name, name, resource_group):
    return call_az("az cosmosdb sql user-defined-function update", locals())


def list(account_name, container_name, database_name, resource_group):
    '''
    List the SQL user defined functions under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql user-defined-function list", locals())


def show(account_name, container_name, database_name, name, resource_group):
    '''
    Show the details of a SQL user defined function under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql user-defined-function show", locals())


def delete(account_name, container_name, database_name, name, resource_group, yes=None):
    '''
    Delete the SQL user defined function under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql user-defined-function delete", locals())

