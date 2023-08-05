from .... pyaz_utils import call_az
from . import keys


def create(name, namespace_name, resource_group, rights=None):
    '''
    Create Authorization Rule for the given Relay Service Namespace
    '''
    return call_az("az relay namespace authorization-rule create", locals())


def show(name, namespace_name, resource_group):
    '''
    Shows the details of Relay Service Namespace Authorization Rule
    '''
    return call_az("az relay namespace authorization-rule show", locals())


def list(namespace_name, resource_group):
    '''
    Shows the list of Authorization Rule by Relay Service Namespace
    '''
    return call_az("az relay namespace authorization-rule list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Authorization Rule of the Relay Service Namespace.
    '''
    return call_az("az relay namespace authorization-rule delete", locals())


def update(name, namespace_name, resource_group, rights, add=None, force_string=None, remove=None, set=None):
    '''
    Updates Authorization Rule for the given Relay Service Namespace
    '''
    return call_az("az relay namespace authorization-rule update", locals())

