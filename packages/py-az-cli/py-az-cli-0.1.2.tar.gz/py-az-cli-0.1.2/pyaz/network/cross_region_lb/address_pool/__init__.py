from .... pyaz_utils import call_az
from . import address


def create(lb_name, name, resource_group, backend_address=None, backend_addresses_config_file=None):
    '''
    Create an address pool.
    '''
    return call_az("az network cross-region-lb address-pool create", locals())


def show(lb_name, name, resource_group):
    return call_az("az network cross-region-lb address-pool show", locals())


def list(lb_name, resource_group):
    return call_az("az network cross-region-lb address-pool list", locals())


def delete(lb_name, name, resource_group):
    '''
    Delete an address pool.
    '''
    return call_az("az network cross-region-lb address-pool delete", locals())

