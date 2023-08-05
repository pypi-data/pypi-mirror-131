from .... pyaz_utils import call_az

def create(managed_instance, resource_group, display_name=None, object_id=None):
    '''
    Creates a new managed instance Active Directory administrator.
    '''
    return call_az("az sql mi ad-admin create", locals())


def list(managed_instance, resource_group):
    '''
    Returns a list of managed instance Active Directory Administrators.
    '''
    return call_az("az sql mi ad-admin list", locals())


def delete(managed_instance, resource_group):
    '''
    Deletes an existing managed instance Active Directory Administrator.
    '''
    return call_az("az sql mi ad-admin delete", locals())


def update(managed_instance, resource_group, display_name=None, object_id=None):
    '''
    Updates an existing managed instance Active Directory administrator.
    '''
    return call_az("az sql mi ad-admin update", locals())

