from .... pyaz_utils import call_az

def list(lb_name, resource_group):
    '''
    List frontend IP addresses.
    '''
    return call_az("az network cross-region-lb frontend-ip list", locals())


def show(lb_name, name, resource_group):
    '''
    Get the details of a frontend IP address.
    '''
    return call_az("az network cross-region-lb frontend-ip show", locals())


def delete(lb_name, name, resource_group):
    '''
    Delete a frontend IP address.
    '''
    return call_az("az network cross-region-lb frontend-ip delete", locals())


def create(lb_name, name, resource_group, public_ip_address=None, public_ip_prefix=None, zone=None):
    '''
    Create a frontend IP address.
    '''
    return call_az("az network cross-region-lb frontend-ip create", locals())


def update(lb_name, name, resource_group, add=None, force_string=None, public_ip_address=None, public_ip_prefix=None, remove=None, set=None):
    '''
    Update a frontend IP address.
    '''
    return call_az("az network cross-region-lb frontend-ip update", locals())

