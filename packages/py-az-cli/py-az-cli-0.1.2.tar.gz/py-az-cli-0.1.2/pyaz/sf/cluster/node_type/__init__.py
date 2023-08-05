from .... pyaz_utils import call_az

def add(capacity, cluster_name, node_type, resource_group, vm_password, vm_user_name, durability_level=None, vm_sku=None, vm_tier=None):
    '''
    Add a new node type to a cluster.
    '''
    return call_az("az sf cluster node-type add", locals())

