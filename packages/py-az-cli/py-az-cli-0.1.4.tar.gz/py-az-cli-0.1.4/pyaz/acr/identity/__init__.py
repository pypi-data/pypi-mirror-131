from ... pyaz_utils import _call_az

def show(name, resource_group=None):
    '''
    Show the container registry's identity details
    '''
    return _call_az("az acr identity show", locals())


def assign(identities, name, resource_group=None):
    '''
    Assign a managed identity to a container registry
    '''
    return _call_az("az acr identity assign", locals())


def remove(identities, name, resource_group=None):
    '''
    Remove a managed identity from a container registry
    '''
    return _call_az("az acr identity remove", locals())

