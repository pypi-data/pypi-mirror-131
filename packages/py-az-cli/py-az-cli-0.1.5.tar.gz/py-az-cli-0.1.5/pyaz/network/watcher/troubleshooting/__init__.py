from .... pyaz_utils import _call_az

def start(resource, storage_account, storage_path, no_wait=None, resource_group=None, resource_type=None):
    '''
    Troubleshoot issues with VPN connections or gateway connectivity.
    '''
    return _call_az("az network watcher troubleshooting start", locals())


def show(resource, resource_group=None, resource_type=None):
    '''
    Get the results of the last troubleshooting operation.
    '''
    return _call_az("az network watcher troubleshooting show", locals())

