from .... pyaz_utils import _call_az

def update(cluster_name, reliability_level, resource_group, auto_add_node=None):
    '''
    Update the reliability tier for the primary node in a cluster.
    '''
    return _call_az("az sf cluster reliability update", locals())

