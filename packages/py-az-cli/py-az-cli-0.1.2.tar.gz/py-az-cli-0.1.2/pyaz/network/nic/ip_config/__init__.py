from .... pyaz_utils import call_az
from . import address_pool, inbound_nat_rule


def create(name, nic_name, resource_group, app_gateway_address_pools=None, application_security_groups=None, gateway_name=None, lb_address_pools=None, lb_inbound_nat_rules=None, lb_name=None, make_primary=None, private_ip_address=None, private_ip_address_version=None, public_ip_address=None, subnet=None, vnet_name=None):
    '''
    Create an IP configuration.
    '''
    return call_az("az network nic ip-config create", locals())


def update(name, nic_name, resource_group, add=None, app_gateway_address_pools=None, application_security_groups=None, force_string=None, gateway_lb=None, gateway_name=None, lb_address_pools=None, lb_inbound_nat_rules=None, lb_name=None, make_primary=None, private_ip_address=None, private_ip_address_version=None, public_ip_address=None, remove=None, set=None, subnet=None, vnet_name=None):
    '''
    Update an IP configuration.
    '''
    return call_az("az network nic ip-config update", locals())


def list(nic_name, resource_group):
    '''
    List the IP configurations of a NIC.
    '''
    return call_az("az network nic ip-config list", locals())


def show(name, nic_name, resource_group):
    '''
    Show the details of an IP configuration.
    '''
    return call_az("az network nic ip-config show", locals())


def delete(name, nic_name, resource_group):
    '''
    Delete an IP configuration.
    '''
    return call_az("az network nic ip-config delete", locals())

