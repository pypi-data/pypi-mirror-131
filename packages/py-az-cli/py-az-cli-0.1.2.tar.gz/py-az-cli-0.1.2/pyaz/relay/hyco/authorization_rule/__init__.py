from .... pyaz_utils import call_az
from . import keys


def create(hybrid_connection_name, name, namespace_name, resource_group, rights=None):
    '''
    Create Authorization Rule for given Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco authorization-rule create", locals())


def show(hybrid_connection_name, name, namespace_name, resource_group):
    '''
    Shows the details of Authorization Rule for given Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco authorization-rule show", locals())


def list(hybrid_connection_name, namespace_name, resource_group):
    '''
    shows list of Authorization Rule by Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco authorization-rule list", locals())


def delete(hybrid_connection_name, name, namespace_name, resource_group):
    '''
    Deletes the Authorization Rule of the given Relay Service Hybrid Connection.
    '''
    return call_az("az relay hyco authorization-rule delete", locals())


def update(hybrid_connection_name, name, namespace_name, resource_group, rights, add=None, force_string=None, remove=None, set=None):
    '''
    Create Authorization Rule for given Relay Service Hybrid Connection
    '''
    return call_az("az relay hyco authorization-rule update", locals())

