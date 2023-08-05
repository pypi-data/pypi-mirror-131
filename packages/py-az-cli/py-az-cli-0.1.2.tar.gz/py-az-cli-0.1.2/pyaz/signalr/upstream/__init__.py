from ... pyaz_utils import call_az

def list(name, resource_group):
    '''
    List upstream settings of an existing SignalR Service.
    '''
    return call_az("az signalr upstream list", locals())


def update(name, resource_group, template):
    '''
    Update order sensitive upstream settings for an existing SignalR Service.
    '''
    return call_az("az signalr upstream update", locals())


def clear(name, resource_group):
    '''
    List upstream settings of an existing SignalR Service.
    '''
    return call_az("az signalr upstream clear", locals())

