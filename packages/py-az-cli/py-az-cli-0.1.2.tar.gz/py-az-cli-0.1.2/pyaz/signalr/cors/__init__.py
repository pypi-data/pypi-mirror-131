from ... pyaz_utils import call_az

def add(allowed_origins, name, resource_group):
    '''
    Add allowed origins to a SignalR Service
    '''
    return call_az("az signalr cors add", locals())


def remove(allowed_origins, name, resource_group):
    '''
    Remove allowed origins from a SignalR Service
    '''
    return call_az("az signalr cors remove", locals())


def list(name, resource_group):
    '''
    List allowed origins of a SignalR Service
    '''
    return call_az("az signalr cors list", locals())


def update(allowed_origins, name, resource_group):
    '''
    Update allowed origins to a SignalR Service
    '''
    return call_az("az signalr cors update", locals())

