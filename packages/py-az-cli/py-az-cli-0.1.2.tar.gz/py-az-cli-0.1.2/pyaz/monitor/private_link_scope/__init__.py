from ... pyaz_utils import call_az
from . import private_endpoint_connection, private_link_resource, scoped_resource


def show(name, resource_group):
    '''
    Show a monitor private link scope resource.
    '''
    return call_az("az monitor private-link-scope show", locals())


def list(resource_group=None):
    '''
    List all monitor private link scope resource.
    '''
    return call_az("az monitor private-link-scope list", locals())


def create(name, resource_group, tags=None):
    '''
    Create a private link scope resource.
    '''
    return call_az("az monitor private-link-scope create", locals())


def update(name, resource_group, tags):
    '''
    Update a monitor private link scope resource.
    '''
    return call_az("az monitor private-link-scope update", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a monitor private link scope resource.
    '''
    return call_az("az monitor private-link-scope delete", locals())

