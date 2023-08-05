from ... pyaz_utils import call_az

def list(name, resource_group):
    '''
    Get the Network access control of SignalR Service.
    '''
    return call_az("az signalr network-rule list", locals())


def update(name, resource_group, allow=None, connection_name=None, deny=None, public_network=None):
    '''
    Update the Network access control of SignalR Service.
    '''
    return call_az("az signalr network-rule update", locals())

