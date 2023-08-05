from .... pyaz_utils import call_az

def create(account_name, body, container_name, database_name, name, resource_group):
    '''
    Create an SQL stored procedure under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql stored-procedure create", locals())


def update(account_name, body, container_name, database_name, name, resource_group):
    return call_az("az cosmosdb sql stored-procedure update", locals())


def list(account_name, container_name, database_name, resource_group):
    '''
    List the SQL stored procedures under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql stored-procedure list", locals())


def show(account_name, container_name, database_name, name, resource_group):
    '''
    Show the details of a SQL stored procedure under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql stored-procedure show", locals())


def delete(account_name, container_name, database_name, name, resource_group, yes=None):
    '''
    Delete the SQL stored procedure under an Azure Cosmos DB SQL container.
    '''
    return call_az("az cosmosdb sql stored-procedure delete", locals())

