from .... pyaz_utils import call_az

def show(resource_group, workspace_name):
    '''
    Get the SQL Azure Active Directory administrator.
    '''
    return call_az("az synapse sql ad-admin show", locals())


def create(display_name, object_id, resource_group, workspace_name, no_wait=None):
    '''
    Create the SQL Azure Active Directory administrator.
    '''
    return call_az("az synapse sql ad-admin create", locals())


def update(resource_group, workspace_name, add=None, display_name=None, force_string=None, no_wait=None, object_id=None, remove=None, set=None):
    '''
    Update the SQL Azure Active Directory administrator.
    '''
    return call_az("az synapse sql ad-admin update", locals())


def delete(resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Delete the SQL Azure Active Directory administrator.
    '''
    return call_az("az synapse sql ad-admin delete", locals())


def wait(resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition is met.
    '''
    return call_az("az synapse sql ad-admin wait", locals())

