from .... pyaz_utils import call_az
from . import keys


def create(name, namespace_name, resource_group, topic_name, rights=None):
    '''
    Create Authorization Rule for given Service Bus Topic
    '''
    return call_az("az servicebus topic authorization-rule create", locals())


def show(name, namespace_name, resource_group, topic_name):
    '''
    Shows the details of Authorization Rule for given Service Bus Topic
    '''
    return call_az("az servicebus topic authorization-rule show", locals())


def list(namespace_name, resource_group, topic_name):
    '''
    shows list of Authorization Rule by Service Bus Topic
    '''
    return call_az("az servicebus topic authorization-rule list", locals())


def delete(name, namespace_name, resource_group, topic_name):
    '''
    Deletes the Authorization Rule of the given Service Bus Topic.
    '''
    return call_az("az servicebus topic authorization-rule delete", locals())


def update(name, namespace_name, resource_group, rights, topic_name, add=None, force_string=None, remove=None, set=None):
    '''
    Create Authorization Rule for given Service Bus Topic
    '''
    return call_az("az servicebus topic authorization-rule update", locals())

