from .... pyaz_utils import call_az

def create(resource_group, server_name, display_name=None, no_wait=None, object_id=None):
    '''
    Create an Active Directory administrator for MySQL server.
    '''
    return call_az("az mysql server ad-admin create", locals())


def list(resource_group, server_name):
    '''
    List all Active Directory Administrators for MySQL server.
    '''
    return call_az("az mysql server ad-admin list", locals())


def delete(resource_group, server_name, yes=None):
    '''
    Delete an Active Directory Administrator for MySQL server.
    '''
    return call_az("az mysql server ad-admin delete", locals())


def show(resource_group, server_name):
    '''
    Get Active Directory Administrator information for a MySQL server.
    '''
    return call_az("az mysql server ad-admin show", locals())


def wait(resource_group, server_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the MySQL server Active Directory Administrator is met.
    '''
    return call_az("az mysql server ad-admin wait", locals())

