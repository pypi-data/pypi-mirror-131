from .... pyaz_utils import call_az
from . import event_channel, key


def show(name, resource_group):
    '''
    Get the details of a partner namespace.
    '''
    return call_az("az eventgrid partner namespace show", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a partner namespace.
    '''
    return call_az("az eventgrid partner namespace delete", locals())


def list(odata_query=None, resource_group=None):
    '''
    List available partner namespaces.
    '''
    return call_az("az eventgrid partner namespace list", locals())


def create(name, partner_registration_id, resource_group, location=None, tags=None):
    '''
    Create a partner namespace.
    '''
    return call_az("az eventgrid partner namespace create", locals())

