from .... pyaz_utils import call_az

def list(cluster, resource_group, workspace):
    '''
    List remote login information for cluster's nodes.
    '''
    return call_az("az batchai cluster node list", locals())


def exec(cluster, resource_group, workspace, address=None, exec=None, node_id=None, password=None, ssh_private_key=None):
    '''
    Executes a command line on a cluster's node with optional ports forwarding.
    '''
    return call_az("az batchai cluster node exec", locals())

