from ... pyaz_utils import call_az

def list(cluster_name, resource_group):
    '''
    List node pools in the managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool list", locals())


def show(cluster_name, name, resource_group):
    '''
    Show the details for a node pool in the managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool show", locals())


def add(cluster_name, name, resource_group, enable_cluster_autoscaler=None, enable_encryption_at_host=None, enable_node_public_ip=None, enable_ultra_ssd=None, eviction_policy=None, kubernetes_version=None, labels=None, max_count=None, max_pods=None, max_surge=None, min_count=None, mode=None, no_wait=None, node_count=None, node_osdisk_size=None, node_osdisk_type=None, node_public_ip_prefix_id=None, node_taints=None, node_vm_size=None, os_sku=None, os_type=None, ppg=None, priority=None, spot_max_price=None, tags=None, vnet_subnet_id=None, zones=None):
    '''
    Add a node pool to the managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool add", locals())


def scale(cluster_name, name, resource_group, no_wait=None, node_count=None):
    '''
    Scale the node pool in a managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool scale", locals())


def upgrade(cluster_name, name, resource_group, kubernetes_version=None, max_surge=None, no_wait=None, node_image_only=None):
    '''
    Upgrade the node pool in a managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool upgrade", locals())


def update(cluster_name, name, resource_group, disable_cluster_autoscaler=None, enable_cluster_autoscaler=None, labels=None, max_count=None, max_surge=None, min_count=None, mode=None, no_wait=None, tags=None, update_cluster_autoscaler=None):
    '''
    Update a node pool to enable/disable cluster-autoscaler or change min-count or max-count
    '''
    return call_az("az aks nodepool update", locals())


def delete(cluster_name, name, resource_group, no_wait=None):
    '''
    Delete the agent pool in the managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool delete", locals())


def get_upgrades(cluster_name, nodepool_name, resource_group):
    '''
    Get the available upgrade versions for an agent pool of the managed Kubernetes cluster.
    '''
    return call_az("az aks nodepool get-upgrades", locals())

