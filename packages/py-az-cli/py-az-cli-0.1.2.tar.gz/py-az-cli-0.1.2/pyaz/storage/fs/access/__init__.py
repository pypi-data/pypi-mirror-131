from .... pyaz_utils import call_az

def set(account_key=None, account_name=None, acl=None, auth_mode=None, connection_string=None, group=None, owner=None, permissions=None, sas_token=None):
    '''
    Set the access control properties of a path(directory or file) in Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs access set", locals())


def show(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None):
    '''
    Show the access control properties of a path (directory or file) in Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs access show", locals())


def set_recursive(acl, account_key=None, account_name=None, auth_mode=None, batch_size=None, connection_string=None, continuation=None, continue_on_failure=None, max_batches=None, sas_token=None, timeout=None):
    '''
    Set the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs access set-recursive", locals())


def update_recursive(acl, account_key=None, account_name=None, auth_mode=None, batch_size=None, connection_string=None, continuation=None, continue_on_failure=None, max_batches=None, sas_token=None, timeout=None):
    '''
    Modify the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs access update-recursive", locals())


def remove_recursive(acl, account_key=None, account_name=None, auth_mode=None, batch_size=None, connection_string=None, continuation=None, continue_on_failure=None, max_batches=None, sas_token=None, timeout=None):
    '''
    Remove the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs access remove-recursive", locals())

