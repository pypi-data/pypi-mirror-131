from .... pyaz_utils import _call_az

def list(name, resource_group):
    '''
    List of Namespaces within given Cluster.
    '''
    return _call_az("az eventhubs cluster namespace list", locals())

