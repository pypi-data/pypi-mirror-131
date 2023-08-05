from .... pyaz_utils import call_az

def create(kid, managed_instance, resource_group):
    '''
    Creates a SQL Instance key.
    '''
    return call_az("az sql mi key create", locals())


def delete(kid, managed_instance, resource_group):
    '''
    Deletes a SQL Instance key.
    '''
    return call_az("az sql mi key delete", locals())


def show(kid, managed_instance, resource_group):
    '''
    Shows a SQL Instance key.
    '''
    return call_az("az sql mi key show", locals())


def list(managed_instance, resource_group, filter=None):
    return call_az("az sql mi key list", locals())

