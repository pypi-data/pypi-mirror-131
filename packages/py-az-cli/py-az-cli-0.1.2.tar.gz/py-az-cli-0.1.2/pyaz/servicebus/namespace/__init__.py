from ... pyaz_utils import call_az
from . import authorization_rule, network_rule


def create(name, resource_group, capacity=None, default_action=None, location=None, sku=None, tags=None):
    '''
    Create a Service Bus Namespace
    '''
    return call_az("az servicebus namespace create", locals())


def show(name, resource_group):
    '''
    Shows the Service Bus Namespace details
    '''
    return call_az("az servicebus namespace show", locals())


def list(resource_group=None):
    '''
    List the Service Bus Namespaces
    '''
    return call_az("az servicebus namespace list", locals())


def delete(name, resource_group):
    '''
    Deletes the Service Bus Namespace
    '''
    return call_az("az servicebus namespace delete", locals())


def exists(name):
    '''
    check for the availability of the given name for the Namespace
    '''
    return call_az("az servicebus namespace exists", locals())


def update(name, resource_group, add=None, capacity=None, default_action=None, force_string=None, remove=None, set=None, sku=None, tags=None):
    '''
    Updates a Service Bus Namespace
    '''
    return call_az("az servicebus namespace update", locals())

