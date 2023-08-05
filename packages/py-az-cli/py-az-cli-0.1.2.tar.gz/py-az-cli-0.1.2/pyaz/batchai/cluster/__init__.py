from ... pyaz_utils import call_az
from . import file, node


def create(name, resource_group, workspace, afs_mount_path=None, afs_name=None, bfs_mount_path=None, bfs_name=None, config_file=None, custom_image=None, generate_ssh_keys=None, image=None, max=None, min=None, nfs=None, nfs_mount_path=None, password=None, setup_task=None, setup_task_output=None, ssh_key=None, storage_account_key=None, storage_account_name=None, subnet=None, target=None, use_auto_storage=None, user_name=None, vm_priority=None, vm_size=None):
    '''
    Create a cluster.
    '''
    return call_az("az batchai cluster create", locals())


def delete(name, resource_group, workspace, no_wait=None, yes=None):
    '''
    Delete a cluster.
    '''
    return call_az("az batchai cluster delete", locals())


def show(name, resource_group, workspace):
    '''
    Show information about a cluster.
    '''
    return call_az("az batchai cluster show", locals())


def list(resource_group, workspace):
    '''
    List clusters.
    '''
    return call_az("az batchai cluster list", locals())


def resize(name, resource_group, target, workspace):
    '''
    Resize a cluster.
    '''
    return call_az("az batchai cluster resize", locals())


def auto_scale(max, min, name, resource_group, workspace):
    '''
    Set auto-scale parameters for a cluster.
    '''
    return call_az("az batchai cluster auto-scale", locals())

