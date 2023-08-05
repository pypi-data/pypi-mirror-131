from .... pyaz_utils import call_az

def set(name, resource_group, server_name, source=None, value=None):
    '''
    Update the parameter of a flexible server.
    '''
    return call_az("az postgres flexible-server parameter set", locals())


def show(name, resource_group, server_name):
    '''
    Get the parameter for a flexible server."
    '''
    return call_az("az postgres flexible-server parameter show", locals())


def list(resource_group, server_name):
    '''
    List the parameter values for a flexible server.
    '''
    return call_az("az postgres flexible-server parameter list", locals())

