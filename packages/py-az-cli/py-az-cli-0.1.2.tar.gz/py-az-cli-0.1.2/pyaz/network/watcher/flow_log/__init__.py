from .... pyaz_utils import call_az

def configure(nsg, enabled=None, format=None, interval=None, log_version=None, resource_group=None, retention=None, storage_account=None, traffic_analytics=None, workspace=None):
    '''
    Configure flow logging on a network security group.
    '''
    return call_az("az network watcher flow-log configure", locals())


def show(location=None, name=None, nsg=None, resource_group=None):
    '''
    Get the flow log configuration of a network security group.
    '''
    return call_az("az network watcher flow-log show", locals())


def list(location):
    '''
    List all flow log resources for the specified Network Watcher
    '''
    return call_az("az network watcher flow-log list", locals())


def delete(location, name):
    '''
    Delete the specified flow log resource.
    '''
    return call_az("az network watcher flow-log delete", locals())


def create(location, name, nsg, enabled=None, format=None, interval=None, log_version=None, resource_group=None, retention=None, storage_account=None, tags=None, traffic_analytics=None, workspace=None):
    '''
    Create a flow log on a network security group.
    '''
    return call_az("az network watcher flow-log create", locals())


def update(location, name, add=None, enabled=None, force_string=None, format=None, interval=None, log_version=None, nsg=None, remove=None, resource_group=None, retention=None, set=None, storage_account=None, tags=None, traffic_analytics=None, workspace=None):
    '''
    Update the flow log configuration of a network security group
    '''
    return call_az("az network watcher flow-log update", locals())

