from .... pyaz_utils import call_az

def create(kid, resource_group, server):
    '''
    Creates a server key.
    '''
    return call_az("az sql server key create", locals())


def delete(kid, resource_group, server):
    '''
    Deletes a server key.
    '''
    return call_az("az sql server key delete", locals())


def show(kid, resource_group, server):
    '''
    Shows a server key.
    '''
    return call_az("az sql server key show", locals())


def list(resource_group, server):
    return call_az("az sql server key list", locals())

