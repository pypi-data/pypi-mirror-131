from .... pyaz_utils import _call_az

def reimage(cluster_name, node_name, resource_group, force=None):
    '''
    Reimage nodes of a node type.
    '''
    return _call_az("az sf managed-node-type node reimage", locals())


def restart(cluster_name, node_name, resource_group, force=None):
    '''
    Restart nodes of a node type.
    '''
    return _call_az("az sf managed-node-type node restart", locals())


def delete(cluster_name, node_name, resource_group, force=None):
    '''
    Delete nodes of a node type.
    '''
    return _call_az("az sf managed-node-type node delete", locals())

