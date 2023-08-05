from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List frontend IP addresses.
    '''
    return call_az("az network application-gateway frontend-ip list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a frontend IP address.
    '''
    return call_az("az network application-gateway frontend-ip show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a frontend IP address.
    '''
    return call_az("az network application-gateway frontend-ip delete", locals())


def create(gateway_name, name, resource_group, no_wait=None, private_ip_address=None, public_ip_address=None, subnet=None, vnet_name=None):
    '''
    Create a frontend IP address.
    '''
    return call_az("az network application-gateway frontend-ip create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, no_wait=None, private_ip_address=None, public_ip_address=None, remove=None, set=None, subnet=None, vnet_name=None):
    '''
    Update a frontend IP address.
    '''
    return call_az("az network application-gateway frontend-ip update", locals())

