from .. pyaz_utils import _call_az

def create(name, resource_group, location=None, tags=None):
    return _call_az("az identity create", locals())


def show(name, resource_group):
    return _call_az("az identity show", locals())


def delete(name, resource_group):
    return _call_az("az identity delete", locals())


def list(resource_group=None):
    '''
    List Managed Service Identities
    '''
    return _call_az("az identity list", locals())


def list_operations():
    '''
    Lists available operations for the Managed Identity provider
    '''
    return _call_az("az identity list-operations", locals())

