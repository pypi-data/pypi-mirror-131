from .. pyaz_utils import call_az
from . import cors, identity, key, network_rule, upstream


def create(name, resource_group, sku, allowed_origins=None, default_action=None, enable_message_logs=None, location=None, service_mode=None, tags=None, unit_count=None):
    '''
    Creates a SignalR Service.
    '''
    return call_az("az signalr create", locals())


def delete(name, resource_group):
    '''
    Deletes a SignalR Service.
    '''
    return call_az("az signalr delete", locals())


def list(resource_group=None):
    '''
    Lists all the SignalR Service under the current subscription.
    '''
    return call_az("az signalr list", locals())


def show(name, resource_group):
    '''
    Get the details of a SignalR Service.
    '''
    return call_az("az signalr show", locals())


def restart(name, resource_group):
    '''
    Restart an existing SignalR Service.
    '''
    return call_az("az signalr restart", locals())


def update(name, resource_group, add=None, allowed_origins=None, default_action=None, enable_message_logs=None, force_string=None, remove=None, service_mode=None, set=None, sku=None, tags=None, unit_count=None):
    '''
    Update an existing SignalR Service.
    '''
    return call_az("az signalr update", locals())

