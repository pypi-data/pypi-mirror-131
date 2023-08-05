from ... pyaz_utils import call_az
from . import peering, subnet


def delete(name, resource_group):
    '''
    Delete a virtual network.
    '''
    return call_az("az network vnet delete", locals())


def list(resource_group=None):
    '''
    List virtual networks.
    '''
    return call_az("az network vnet list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a virtual network.
    '''
    return call_az("az network vnet show", locals())


def check_ip_address(ip_address, name, resource_group):
    '''
    Check if a private IP address is available for use within a virtual network.
    '''
    return call_az("az network vnet check-ip-address", locals())


def create(name, resource_group, address_prefixes=None, bgp_community=None, ddos_protection=None, ddos_protection_plan=None, dns_servers=None, edge_zone=None, enable_encryption=None, encryption_enforcement_policy=None, flowtimeout=None, location=None, network_security_group=None, subnet_name=None, subnet_prefixes=None, tags=None, vm_protection=None):
    '''
    Create a virtual network.
    '''
    return call_az("az network vnet create", locals())


def update(name, resource_group, add=None, address_prefixes=None, bgp_community=None, ddos_protection=None, ddos_protection_plan=None, dns_servers=None, enable_encryption=None, encryption_enforcement_policy=None, flowtimeout=None, force_string=None, remove=None, set=None, vm_protection=None):
    '''
    Update a virtual network.
    '''
    return call_az("az network vnet update", locals())


def list_endpoint_services(location):
    '''
    List which services support VNET service tunneling in a given region.
    '''
    return call_az("az network vnet list-endpoint-services", locals())


def list_available_ips(name, resource_group):
    '''
    List some available ips in the vnet.
    '''
    return call_az("az network vnet list-available-ips", locals())

