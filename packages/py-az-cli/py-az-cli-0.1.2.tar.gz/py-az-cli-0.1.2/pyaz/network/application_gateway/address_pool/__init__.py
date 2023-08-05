from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List address pools.
    '''
    return call_az("az network application-gateway address-pool list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of an address pool.
    '''
    return call_az("az network application-gateway address-pool show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete an address pool.
    '''
    return call_az("az network application-gateway address-pool delete", locals())


def create(gateway_name, name, resource_group, no_wait=None, servers=None):
    '''
    Create an address pool.
    '''
    return call_az("az network application-gateway address-pool create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, no_wait=None, remove=None, servers=None, set=None):
    '''
    Update an address pool.
    '''
    return call_az("az network application-gateway address-pool update", locals())

