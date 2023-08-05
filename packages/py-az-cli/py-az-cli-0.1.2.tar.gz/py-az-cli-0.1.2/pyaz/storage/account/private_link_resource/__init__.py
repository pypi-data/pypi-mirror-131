from .... pyaz_utils import call_az

def list(account_name, resource_group):
    '''
    Get the private link resources that need to be created for a storage account.
    '''
    return call_az("az storage account private-link-resource list", locals())

