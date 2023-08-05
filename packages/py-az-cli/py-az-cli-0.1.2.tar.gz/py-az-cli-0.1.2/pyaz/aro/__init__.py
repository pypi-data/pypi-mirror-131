from .. pyaz_utils import call_az

def create(master_subnet, name, resource_group, worker_subnet, apiserver_visibility=None, client_id=None, client_secret=None, cluster_resource_group=None, domain=None, ingress_visibility=None, location=None, master_vm_size=None, no_wait=None, pod_cidr=None, pull_secret=None, service_cidr=None, tags=None, vnet=None, vnet_resource_group=None, worker_count=None, worker_vm_disk_size_gb=None, worker_vm_size=None):
    '''
    Create a cluster.
    '''
    return call_az("az aro create", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a cluster.
    '''
    return call_az("az aro delete", locals())


def list(resource_group=None):
    '''
    List clusters.
    '''
    return call_az("az aro list", locals())


def show(name, resource_group):
    '''
    Get the details of a cluster.
    '''
    return call_az("az aro show", locals())


def update(name, resource_group, client_id=None, client_secret=None, no_wait=None, refresh_credentials=None):
    '''
    Update a cluster.
    '''
    return call_az("az aro update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for a cluster to reach a desired state.
    '''
    return call_az("az aro wait", locals())


def list_credentials(name, resource_group):
    '''
    List credentials of a cluster.
    '''
    return call_az("az aro list-credentials", locals())

