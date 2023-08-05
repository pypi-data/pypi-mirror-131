from .... pyaz_utils import call_az
from . import keys


def create(eventhub_name, name, namespace_name, resource_group, rights=None):
    '''
    Creates Authorizationrule for the given Eventhub
    '''
    return call_az("az eventhubs eventhub authorization-rule create", locals())


def show(eventhub_name, name, namespace_name, resource_group):
    '''
    shows the details of Authorizationrule
    '''
    return call_az("az eventhubs eventhub authorization-rule show", locals())


def list(eventhub_name, namespace_name, resource_group):
    '''
    shows the list of Authorization-rules by Eventhub
    '''
    return call_az("az eventhubs eventhub authorization-rule list", locals())


def delete(eventhub_name, name, namespace_name, resource_group):
    '''
    Deletes the Authorizationrule of Eventhub.
    '''
    return call_az("az eventhubs eventhub authorization-rule delete", locals())


def update(eventhub_name, name, namespace_name, resource_group, rights, add=None, force_string=None, remove=None, set=None):
    '''
    Updates Authorizationrule for the given Eventhub
    '''
    return call_az("az eventhubs eventhub authorization-rule update", locals())

