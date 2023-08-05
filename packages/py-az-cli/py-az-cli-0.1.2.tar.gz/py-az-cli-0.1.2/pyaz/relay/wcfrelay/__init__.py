from ... pyaz_utils import call_az
from . import authorization_rule


def create(name, namespace_name, relay_type, resource_group, requires_client_authorization=None, requires_transport_security=None, user_metadata=None):
    '''
    Create the Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay create", locals())


def show(name, namespace_name, resource_group):
    '''
    shows the Relay Service WCF Relay Details
    '''
    return call_az("az relay wcfrelay show", locals())


def list(namespace_name, resource_group):
    '''
    List the WCF Relay by Relay Service Namespace
    '''
    return call_az("az relay wcfrelay list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay delete", locals())


def update(name, namespace_name, resource_group, add=None, force_string=None, relay_type=None, remove=None, set=None, status=None, user_metadata=None):
    '''
    Updates existing Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay update", locals())

