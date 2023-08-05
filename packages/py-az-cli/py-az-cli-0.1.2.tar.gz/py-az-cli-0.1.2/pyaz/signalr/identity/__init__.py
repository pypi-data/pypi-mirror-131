from ... pyaz_utils import call_az

def assign(identity, name, resource_group):
    '''
    Assign managed identity for SignalR Service.
    '''
    return call_az("az signalr identity assign", locals())


def remove(name, resource_group):
    '''
    Remove managed identity for SignalR Service.
    '''
    return call_az("az signalr identity remove", locals())


def show(name, resource_group):
    '''
    Show managed identity for SignalR Service.
    '''
    return call_az("az signalr identity show", locals())

