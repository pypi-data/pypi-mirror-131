from .... pyaz_utils import call_az

def show(account_name, resource_group):
    '''
    Get the data policy rules associated with the specified storage account.
    '''
    return call_az("az storage account management-policy show", locals())


def create(account_name, policy, resource_group):
    '''
    Create the data policy rules associated with the specified storage account.
    '''
    return call_az("az storage account management-policy create", locals())


def update(account_name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update the data policy rules associated with the specified storage account.
    '''
    return call_az("az storage account management-policy update", locals())


def delete(account_name, resource_group):
    '''
    Delete the data policy rules associated with the specified storage account.
    '''
    return call_az("az storage account management-policy delete", locals())

