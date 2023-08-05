from ... pyaz_utils import call_az

def create(file, name, workspace_name, no_wait=None):
    '''
    Create a linked service.
    '''
    return call_az("az synapse linked-service create", locals())


def set(file, name, workspace_name, no_wait=None):
    '''
    Update an exist linked service.
    '''
    return call_az("az synapse linked-service set", locals())


def update(file, name, workspace_name, no_wait=None):
    '''
    Update an exist linked service.
    '''
    return call_az("az synapse linked-service update", locals())


def list(workspace_name):
    '''
    List linked services.
    '''
    return call_az("az synapse linked-service list", locals())


def show(name, workspace_name):
    '''
    Get a linked service.
    '''
    return call_az("az synapse linked-service show", locals())


def delete(name, workspace_name, no_wait=None, yes=None):
    '''
    Delete a linked service.
    '''
    return call_az("az synapse linked-service delete", locals())

