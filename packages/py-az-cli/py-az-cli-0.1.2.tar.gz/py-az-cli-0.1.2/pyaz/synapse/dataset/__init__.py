from ... pyaz_utils import call_az

def create(file, name, workspace_name, no_wait=None):
    '''
    Create a dataset.
    '''
    return call_az("az synapse dataset create", locals())


def set(file, name, workspace_name, no_wait=None):
    '''
    Update an exist dataset.
    '''
    return call_az("az synapse dataset set", locals())


def update(file, name, workspace_name, no_wait=None):
    '''
    Update an exist dataset.
    '''
    return call_az("az synapse dataset update", locals())


def list(workspace_name):
    '''
    List datasets.
    '''
    return call_az("az synapse dataset list", locals())


def show(name, workspace_name):
    '''
    Get a dataset.
    '''
    return call_az("az synapse dataset show", locals())


def delete(name, workspace_name, no_wait=None, yes=None):
    '''
    Delete a dataset.
    '''
    return call_az("az synapse dataset delete", locals())

