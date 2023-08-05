from .... pyaz_utils import call_az

def create(resource_group, server_name, display_name=None, object_id=None):
    '''
    Create a new server Active Directory administrator.
    '''
    return call_az("az sql server ad-admin create", locals())


def list(resource_group, server_name):
    return call_az("az sql server ad-admin list", locals())


def delete(resource_group, server_name):
    return call_az("az sql server ad-admin delete", locals())


def update(resource_group, server_name, add=None, display_name=None, force_string=None, object_id=None, remove=None, set=None):
    '''
    Update an existing server Active Directory administrator.
    '''
    return call_az("az sql server ad-admin update", locals())

