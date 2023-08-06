from .... pyaz_utils import _call_az

def set(cluster_name, resource_group, upgrade_mode, version=None):
    '''
    Change the  upgrade type for a cluster.
    '''
    return _call_az("az sf cluster upgrade-type set", locals())

