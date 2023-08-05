from .... pyaz_utils import call_az

def add(cluster_name, node_type, number_of_nodes_to_add, resource_group):
    '''
    Add nodes to a node type in a cluster.
    '''
    return call_az("az sf cluster node add", locals())


def remove(cluster_name, node_type, number_of_nodes_to_remove, resource_group):
    '''
    Remove nodes from a node type in a cluster.
    '''
    return call_az("az sf cluster node remove", locals())

