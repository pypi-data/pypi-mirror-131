from .... pyaz_utils import call_az

def create(account_name, name, require_infrastructure_encryption=None, resource_group=None):
    '''
    Create an encryption scope within storage account.
    '''
    return call_az("az storage account encryption-scope create", locals())


def show(account_name, name, resource_group=None):
    '''
    Show properties for specified encryption scope within storage account.
    '''
    return call_az("az storage account encryption-scope show", locals())


def list(account_name, resource_group=None):
    '''
    List encryption scopes within storage account.
    '''
    return call_az("az storage account encryption-scope list", locals())


def update(account_name, name, resource_group=None, state=None):
    '''
    Update properties for specified encryption scope within storage account.
    '''
    return call_az("az storage account encryption-scope update", locals())

