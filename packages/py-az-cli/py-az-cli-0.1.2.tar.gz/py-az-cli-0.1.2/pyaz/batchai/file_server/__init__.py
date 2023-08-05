from ... pyaz_utils import call_az

def create(name, resource_group, workspace, caching_type=None, config_file=None, disk_count=None, disk_size=None, generate_ssh_keys=None, no_wait=None, password=None, ssh_key=None, storage_sku=None, subnet=None, user_name=None, vm_size=None):
    '''
    Create a file server.
    '''
    return call_az("az batchai file-server create", locals())


def list(resource_group, workspace):
    '''
    List file servers.
    '''
    return call_az("az batchai file-server list", locals())

