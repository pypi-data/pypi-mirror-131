from ..... pyaz_utils import call_az

def add(connection_monitor, location, type, workspace_id=None):
    '''
    Add an output to a connection monitor
    '''
    return call_az("az network watcher connection-monitor output add", locals())


def remove(connection_monitor, location):
    '''
    Remove all outputs from a connection monitor
    '''
    return call_az("az network watcher connection-monitor output remove", locals())


def list(connection_monitor, location):
    '''
    List all output from a connection monitor
    '''
    return call_az("az network watcher connection-monitor output list", locals())

