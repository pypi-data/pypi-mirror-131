from ... pyaz_utils import call_az
from . import authorization_rule


def create(name, namespace_name, resource_group, requires_client_authorization=None, user_metadata=None):
    '''
    Create the Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco create", locals())


def show(name, namespace_name, resource_group):
    '''
    Shows the Relay Service Hybrid Connection Details
    '''
    return call_az("az relay hyco show", locals())


def list(namespace_name, resource_group):
    '''
    List the Hybrid Connection by Relay Service Namespace
    '''
    return call_az("az relay hyco list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco delete", locals())


def update(name, namespace_name, resource_group, add=None, force_string=None, remove=None, requires_client_authorization=None, set=None, status=None, user_metadata=None):
    '''
    Updates the Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco update", locals())

