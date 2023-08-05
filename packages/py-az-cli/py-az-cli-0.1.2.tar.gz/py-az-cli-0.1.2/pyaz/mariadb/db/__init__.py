from ... pyaz_utils import call_az

def create(name, resource_group, server_name, charset=None, collation=None):
    '''
    Create a MariaDB database.
    '''
    return call_az("az mariadb db create", locals())


def delete(name, resource_group, server_name, yes=None):
    '''
    Delete a database.
    '''
    return call_az("az mariadb db delete", locals())


def show(name, resource_group, server_name):
    '''
    Show the details of a database.
    '''
    return call_az("az mariadb db show", locals())


def list(resource_group, server_name):
    '''
    List the databases for a server.
    '''
    return call_az("az mariadb db list", locals())

