from .... pyaz_utils import call_az

def assign(name, registry, identities=None, resource_group=None):
    '''
    Update the managed identity for a task.
    '''
    return call_az("az acr task identity assign", locals())


def remove(name, registry, identities=None, resource_group=None):
    '''
    Remove managed identities for a task.
    '''
    return call_az("az acr task identity remove", locals())


def show(name, registry, resource_group=None):
    '''
    Display the managed identities for task.
    '''
    return call_az("az acr task identity show", locals())

