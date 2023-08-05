from .... pyaz_utils import call_az

def add(login_server, name, registry, password=None, resource_group=None, use_identity=None, username=None):
    '''
    Add a custom registry login credential to the task
    '''
    return call_az("az acr task credential add", locals())


def update(login_server, name, registry, password=None, resource_group=None, use_identity=None, username=None):
    '''
    Update the registry login credential for a task.
    '''
    return call_az("az acr task credential update", locals())


def remove(login_server, name, registry, resource_group=None):
    '''
    Remove credential for a task.
    '''
    return call_az("az acr task credential remove", locals())


def list(name, registry, resource_group=None):
    '''
    List all the custom registry credentials for task.
    '''
    return call_az("az acr task credential list", locals())

