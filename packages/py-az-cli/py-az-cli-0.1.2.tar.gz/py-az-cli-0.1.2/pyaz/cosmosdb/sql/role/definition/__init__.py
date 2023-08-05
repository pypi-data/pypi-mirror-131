from ..... pyaz_utils import call_az

def create(account_name, body, resource_group, no_wait=None):
    '''
    Create a SQL role definition under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb sql role definition create", locals())


def update(account_name, body, resource_group, no_wait=None):
    '''
    Update a SQL role definition under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb sql role definition update", locals())


def exists(account_name, id, resource_group):
    '''
    Check if an Azure Cosmos DB role definition exists.
    '''
    return call_az("az cosmosdb sql role definition exists", locals())


def list(account_name, resource_group):
    '''
    List all SQL role definitions under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb sql role definition list", locals())


def show(account_name, id, resource_group):
    '''
    Show the properties of a SQL role definition under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb sql role definition show", locals())


def delete(account_name, id, resource_group, no_wait=None, yes=None):
    '''
    Delete a SQL role definition under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb sql role definition delete", locals())


def wait(account_name, id, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Poll on a SQL role definition until a specific condition is met.
    '''
    return call_az("az cosmosdb sql role definition wait", locals())

