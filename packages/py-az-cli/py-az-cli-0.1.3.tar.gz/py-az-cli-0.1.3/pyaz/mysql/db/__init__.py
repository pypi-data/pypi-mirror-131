from ... pyaz_utils import _call_az

def create(name, resource_group, server_name, charset=None, collation=None):
    '''
    Create a MySQL database.
    '''
    return _call_az("az mysql db create", locals())


def delete(name, resource_group, server_name, yes=None):
    '''
    Delete a database.
    '''
    return _call_az("az mysql db delete", locals())


def show(name, resource_group, server_name):
    '''
    Show the details of a database.
    '''
    return _call_az("az mysql db show", locals())


def list(resource_group, server_name):
    '''
    List the databases for a server.
    '''
    return _call_az("az mysql db list", locals())

