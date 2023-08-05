from ... pyaz_utils import call_az

def show(db_name, key=None, name=None, resource_group_name=None, url_connection=None):
    '''
    Shows an Azure Cosmos DB database
    '''
    return call_az("az cosmosdb database show", locals())


def list(key=None, name=None, resource_group_name=None, url_connection=None):
    '''
    Lists all Azure Cosmos DB databases
    '''
    return call_az("az cosmosdb database list", locals())


def exists(db_name, key=None, name=None, resource_group_name=None, url_connection=None):
    '''
    Returns a boolean indicating whether the database exists
    '''
    return call_az("az cosmosdb database exists", locals())


def create(db_name, key=None, name=None, resource_group_name=None, throughput=None, url_connection=None):
    '''
    Creates an Azure Cosmos DB database
    '''
    return call_az("az cosmosdb database create", locals())


def delete(db_name, key=None, name=None, resource_group_name=None, url_connection=None, yes=None):
    '''
    Deletes an Azure Cosmos DB database
    '''
    return call_az("az cosmosdb database delete", locals())

