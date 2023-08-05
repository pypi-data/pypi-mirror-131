from .... pyaz_utils import call_az

def list(resource_group, workspace_name):
    '''
    List keys under specified workspace.
    '''
    return call_az("az synapse workspace key list", locals())


def show(name, resource_group, workspace_name):
    '''
    Show a workspace's key by name.
    '''
    return call_az("az synapse workspace key show", locals())


def create(key_identifier, name, resource_group, workspace_name, no_wait=None):
    '''
    Create a workspace's key.
    '''
    return call_az("az synapse workspace key create", locals())


def delete(name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Delete a workspace's key. The key at active status can't be deleted.
    '''
    return call_az("az synapse workspace key delete", locals())


def wait(key_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a workspace key is met.
    '''
    return call_az("az synapse workspace key wait", locals())

