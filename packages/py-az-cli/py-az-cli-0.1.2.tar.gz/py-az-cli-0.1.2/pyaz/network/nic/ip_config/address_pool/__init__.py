from ..... pyaz_utils import call_az

def add(address_pool, ip_config_name, nic_name, resource_group, gateway_name=None, lb_name=None):
    '''
    Add an address pool to an IP configuration.
    '''
    return call_az("az network nic ip-config address-pool add", locals())


def remove(address_pool, ip_config_name, nic_name, resource_group, gateway_name=None, lb_name=None):
    '''
    Remove an address pool of an IP configuration.
    '''
    return call_az("az network nic ip-config address-pool remove", locals())

