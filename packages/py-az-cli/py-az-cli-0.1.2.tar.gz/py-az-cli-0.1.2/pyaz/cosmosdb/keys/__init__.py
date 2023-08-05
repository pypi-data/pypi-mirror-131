from ... pyaz_utils import call_az

def list(name, resource_group, type=None):
    '''
    List the access keys or connection strings for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb keys list", locals())


def regenerate(key_kind, name, resource_group):
    '''
    Regenerate an access key for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb keys regenerate", locals())

