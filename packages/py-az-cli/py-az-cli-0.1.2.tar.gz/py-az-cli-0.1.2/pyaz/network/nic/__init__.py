from ... pyaz_utils import call_az
from . import ip_config


def create(name, resource_group, subnet, accelerated_networking=None, app_gateway_address_pools=None, application_security_groups=None, dns_servers=None, edge_zone=None, gateway_name=None, internal_dns_name=None, ip_forwarding=None, lb_address_pools=None, lb_inbound_nat_rules=None, lb_name=None, location=None, network_security_group=None, no_wait=None, private_ip_address=None, private_ip_address_version=None, public_ip_address=None, tags=None, vnet_name=None):
    '''
    Create a network interface.
    '''
    return call_az("az network nic create", locals())


def delete(name, resource_group, no_wait=None):
    '''
    Delete a network interface.
    '''
    return call_az("az network nic delete", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a network interface.
    '''
    return call_az("az network nic show", locals())


def list(resource_group=None):
    '''
    List network interfaces.
    '''
    return call_az("az network nic list", locals())


def show_effective_route_table(name, resource_group):
    '''
    Show the effective route table applied to a network interface.
    '''
    return call_az("az network nic show-effective-route-table", locals())


def list_effective_nsg(name, resource_group):
    '''
    List all effective network security groups applied to a network interface.
    '''
    return call_az("az network nic list-effective-nsg", locals())


def update(name, resource_group, accelerated_networking=None, add=None, dns_servers=None, force_string=None, internal_dns_name=None, ip_forwarding=None, network_security_group=None, no_wait=None, remove=None, set=None):
    '''
    Update a network interface.
    '''
    return call_az("az network nic update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the network interface is met.
    '''
    return call_az("az network nic wait", locals())

