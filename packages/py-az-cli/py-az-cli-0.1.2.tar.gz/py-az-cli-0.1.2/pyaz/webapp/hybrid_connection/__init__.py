from ... pyaz_utils import call_az

def list(name, resource_group, slot=None):
    '''
    list the hybrid-connections on a webapp
    '''
    return call_az("az webapp hybrid-connection list", locals())


def add(hybrid_connection, name, namespace, resource_group, slot=None):
    '''
    add an existing hybrid-connection to a webapp
    '''
    return call_az("az webapp hybrid-connection add", locals())


def remove(hybrid_connection, name, namespace, resource_group, slot=None):
    '''
    remove a hybrid-connection from a webapp
    '''
    return call_az("az webapp hybrid-connection remove", locals())

