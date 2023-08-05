from ... pyaz_utils import call_az
from . import authorization_rule


def create(name, resource_group, location=None, tags=None):
    '''
    Create a Relay Service Namespace
    '''
    return call_az("az relay namespace create", locals())


def show(name, resource_group):
    '''
    Shows the Relay Service Namespace details
    '''
    return call_az("az relay namespace show", locals())


def list(resource_group=None):
    '''
    List the Relay Service Namespaces
    '''
    return call_az("az relay namespace list", locals())


def delete(name, resource_group):
    '''
    Deletes the Relay Service Namespace
    '''
    return call_az("az relay namespace delete", locals())


def exists(name):
    '''
    check for the availability of the given name for the Namespace
    '''
    return call_az("az relay namespace exists", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Updates a Relay Service Namespace
    '''
    return call_az("az relay namespace update", locals())

