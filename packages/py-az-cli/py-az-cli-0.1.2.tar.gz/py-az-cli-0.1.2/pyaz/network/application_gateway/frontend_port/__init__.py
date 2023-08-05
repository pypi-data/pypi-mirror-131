from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List frontend ports.
    '''
    return call_az("az network application-gateway frontend-port list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a frontend port.
    '''
    return call_az("az network application-gateway frontend-port show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a frontend port.
    '''
    return call_az("az network application-gateway frontend-port delete", locals())


def create(gateway_name, name, port, resource_group, no_wait=None):
    '''
    Create a frontend port.
    '''
    return call_az("az network application-gateway frontend-port create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, no_wait=None, port=None, remove=None, set=None):
    '''
    Update a frontend port.
    '''
    return call_az("az network application-gateway frontend-port update", locals())

