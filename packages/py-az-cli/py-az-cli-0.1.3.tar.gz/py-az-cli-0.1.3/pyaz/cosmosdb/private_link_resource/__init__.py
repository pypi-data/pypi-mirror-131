from ... pyaz_utils import _call_az

def list(account_name, resource_group):
    '''
    List the private link resources supported for Azure Cosmos DB.
    '''
    return _call_az("az cosmosdb private-link-resource list", locals())

