from ... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Show the identities for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb identity show", locals())


def assign(name, resource_group, identities=None):
    '''
    Assign SystemAssigned identity for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb identity assign", locals())


def remove(name, resource_group, identities=None):
    '''
    Remove SystemAssigned identity for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb identity remove", locals())

