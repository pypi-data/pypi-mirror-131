from .... pyaz_utils import call_az

def update(cluster_name, durability_level, node_type, resource_group):
    '''
    Update the durability tier or VM SKU of a node type in the cluster.
    '''
    return call_az("az sf cluster durability update", locals())

