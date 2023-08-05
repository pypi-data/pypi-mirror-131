from ..... pyaz_utils import call_az

def create(name, resource_group, workspace_name, no_wait=None, resource_id=None, write_access_resource_id=None):
    '''
    Create a linked service.
    '''
    return call_az("az monitor log-analytics workspace linked-service create", locals())


def update(name, resource_group, workspace_name, add=None, force_string=None, no_wait=None, remove=None, resource_id=None, set=None, write_access_resource_id=None):
    '''
    Update a linked service.
    '''
    return call_az("az monitor log-analytics workspace linked-service update", locals())


def show(name, resource_group, workspace_name):
    '''
    Show the properties of a linked service.
    '''
    return call_az("az monitor log-analytics workspace linked-service show", locals())


def list(resource_group, workspace_name):
    '''
    Gets all the linked services in a workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-service list", locals())


def delete(name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Delete a linked service.
    '''
    return call_az("az monitor log-analytics workspace linked-service delete", locals())


def wait(name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the linked service is met.
    '''
    return call_az("az monitor log-analytics workspace linked-service wait", locals())

