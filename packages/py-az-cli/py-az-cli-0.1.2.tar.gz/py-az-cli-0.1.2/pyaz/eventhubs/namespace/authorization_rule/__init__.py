from .... pyaz_utils import call_az
from . import keys


def create(name, namespace_name, resource_group, rights=None):
    '''
    Creates Authorizationrule for the given Namespace
    '''
    return call_az("az eventhubs namespace authorization-rule create", locals())


def show(name, namespace_name, resource_group):
    '''
    Shows the details of Authorizationrule
    '''
    return call_az("az eventhubs namespace authorization-rule show", locals())


def list(namespace_name, resource_group):
    '''
    Shows the list of Authorizationrule by Namespace
    '''
    return call_az("az eventhubs namespace authorization-rule list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Authorizationrule of the namespace.
    '''
    return call_az("az eventhubs namespace authorization-rule delete", locals())


def update(name, namespace_name, resource_group, rights, add=None, force_string=None, remove=None, set=None):
    '''
    Updates Authorizationrule for the given Namespace
    '''
    return call_az("az eventhubs namespace authorization-rule update", locals())

