from .... pyaz_utils import call_az
from . import address, tunnel_interface


def create(lb_name, name, resource_group, backend_address=None, backend_addresses_config_file=None, vnet=None):
    '''
    Create an address pool.
    '''
    return call_az("az network lb address-pool create", locals())


def update(lb_name, name, resource_group, add=None, backend_address=None, backend_addresses_config_file=None, force_string=None, remove=None, set=None, vnet=None):
    '''
    Update an address pool.
    '''
    return call_az("az network lb address-pool update", locals())


def show(lb_name, name, resource_group):
    '''
    Get the details of an address pool.
    '''
    return call_az("az network lb address-pool show", locals())


def list(lb_name, resource_group):
    '''
    List address pools.
    '''
    return call_az("az network lb address-pool list", locals())


def delete(lb_name, name, resource_group):
    '''
    Delete an address pool.
    '''
    return call_az("az network lb address-pool delete", locals())

