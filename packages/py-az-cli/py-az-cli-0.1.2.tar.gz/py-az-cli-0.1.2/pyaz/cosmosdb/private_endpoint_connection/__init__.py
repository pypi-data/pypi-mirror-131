from ... pyaz_utils import call_az

def approve(account_name=None, description=None, id=None, name=None, resource_group=None):
    '''
    Approve the specified private endpoint connection associated with Azure Cosmos DB.
    '''
    return call_az("az cosmosdb private-endpoint-connection approve", locals())


def reject(account_name=None, description=None, id=None, name=None, resource_group=None):
    '''
    Reject the specified private endpoint connection associated with Azure Cosmos DB.
    '''
    return call_az("az cosmosdb private-endpoint-connection reject", locals())


def delete(account_name=None, id=None, name=None, resource_group=None):
    '''
    Delete the specified private endpoint connection associated with Azure Cosmos DB.
    '''
    return call_az("az cosmosdb private-endpoint-connection delete", locals())


def show(account_name=None, id=None, name=None, resource_group=None):
    '''
    Show details of a private endpoint connection associated with Azure Cosmos DB.
    '''
    return call_az("az cosmosdb private-endpoint-connection show", locals())

