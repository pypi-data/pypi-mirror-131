from .. pyaz_utils import call_az

def create(name, resource_group, location=None, tags=None):
    return call_az("az identity create", locals())


def show(name, resource_group):
    return call_az("az identity show", locals())


def delete(name, resource_group):
    return call_az("az identity delete", locals())


def list(resource_group=None):
    '''
    List Managed Service Identities
    '''
    return call_az("az identity list", locals())


def list_operations():
    '''
    Lists available operations for the Managed Identity provider
    '''
    return call_az("az identity list-operations", locals())

