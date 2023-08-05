from .... pyaz_utils import call_az
from . import keys


def create(name, namespace_name, relay_name, resource_group, rights=None):
    '''
    Create Authorization Rule for the given Relay Service WCF Relay.
    '''
    return call_az("az relay wcfrelay authorization-rule create", locals())


def show(name, namespace_name, relay_name, resource_group):
    '''
    show properties of Authorization Rule for the given Relay Service WCF Relay.
    '''
    return call_az("az relay wcfrelay authorization-rule show", locals())


def list(namespace_name, relay_name, resource_group):
    '''
    List of Authorization Rule by Relay Service WCF Relay.
    '''
    return call_az("az relay wcfrelay authorization-rule list", locals())


def delete(name, namespace_name, relay_name, resource_group):
    '''
    Delete the Authorization Rule of Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay authorization-rule delete", locals())


def update(name, namespace_name, relay_name, resource_group, rights, add=None, force_string=None, remove=None, set=None):
    '''
    Update Authorization Rule for the given Relay Service WCF Relay.
    '''
    return call_az("az relay wcfrelay authorization-rule update", locals())

