from .... pyaz_utils import call_az

def create(account, credential_name, database_name, uri, user_name, password=None):
    '''
    Create a new catalog credential for use with an external data source.
    '''
    return call_az("az dla catalog credential create", locals())


def show(account, credential_name, database_name):
    '''
    Retrieve a catalog credential.
    '''
    return call_az("az dla catalog credential show", locals())


def update(account, credential_name, database_name, uri, user_name, new_password=None, password=None):
    '''
    Update a catalog credential for use with an external data source.
    '''
    return call_az("az dla catalog credential update", locals())


def list(account, database_name, count=None, filter=None, orderby=None, select=None, skip=None, top=None):
    '''
    List catalog credentials.
    '''
    return call_az("az dla catalog credential list", locals())


def delete(account, credential_name, database_name, cascade=None, password=None):
    '''
    Delete a catalog credential.
    '''
    return call_az("az dla catalog credential delete", locals())

