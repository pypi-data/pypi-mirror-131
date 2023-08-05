from .... pyaz_utils import call_az

def list(name, resource_group):
    '''
    List of Namespaces within given Cluster.
    '''
    return call_az("az eventhubs cluster namespace list", locals())

