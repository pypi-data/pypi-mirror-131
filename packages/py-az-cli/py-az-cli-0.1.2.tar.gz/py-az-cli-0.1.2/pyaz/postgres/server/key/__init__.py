from .... pyaz_utils import call_az

def create(kid, name, resource_group):
    '''
    Create server key.
    '''
    return call_az("az postgres server key create", locals())


def delete(kid, name, resource_group, yes=None):
    '''
    Delete server key.
    '''
    return call_az("az postgres server key delete", locals())


def show(kid, name, resource_group):
    '''
    Show server key.
    '''
    return call_az("az postgres server key show", locals())


def list(name, resource_group):
    return call_az("az postgres server key list", locals())

