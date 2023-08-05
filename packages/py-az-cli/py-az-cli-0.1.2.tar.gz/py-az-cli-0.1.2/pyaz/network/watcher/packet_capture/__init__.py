from .... pyaz_utils import call_az

def create(name, resource_group, vm, capture_limit=None, capture_size=None, file_path=None, filters=None, storage_account=None, storage_path=None, time_limit=None):
    '''
    Create and start a packet capture session.
    '''
    return call_az("az network watcher packet-capture create", locals())


def show(location, name, network_watcher_name=None):
    '''
    Show details of a packet capture session.
    '''
    return call_az("az network watcher packet-capture show", locals())


def show_status(location, name, network_watcher_name=None):
    '''
    Show the status of a packet capture session.
    '''
    return call_az("az network watcher packet-capture show-status", locals())


def delete(location, name, network_watcher_name=None):
    '''
    Delete a packet capture session.
    '''
    return call_az("az network watcher packet-capture delete", locals())


def stop(location, name, network_watcher_name=None):
    '''
    Stop a running packet capture session.
    '''
    return call_az("az network watcher packet-capture stop", locals())


def list(location, network_watcher_name=None):
    '''
    List all packet capture sessions within a resource group.
    '''
    return call_az("az network watcher packet-capture list", locals())

