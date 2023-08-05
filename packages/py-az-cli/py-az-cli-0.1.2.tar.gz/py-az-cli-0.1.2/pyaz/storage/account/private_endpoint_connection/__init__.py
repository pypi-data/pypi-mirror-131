from .... pyaz_utils import call_az

def delete(account_name=None, id=None, name=None, resource_group=None, yes=None):
    '''
    Delete a private endpoint connection request for storage account.
    '''
    return call_az("az storage account private-endpoint-connection delete", locals())


def show(account_name=None, id=None, name=None, resource_group=None):
    '''
    Show details of a private endpoint connection request for storage account.
    '''
    return call_az("az storage account private-endpoint-connection show", locals())


def approve(account_name=None, description=None, id=None, name=None, resource_group=None):
    '''
    Approve a private endpoint connection request for storage account.
    '''
    return call_az("az storage account private-endpoint-connection approve", locals())


def reject(account_name=None, description=None, id=None, name=None, resource_group=None):
    '''
    Reject a private endpoint connection request for storage account.
    '''
    return call_az("az storage account private-endpoint-connection reject", locals())

