from ... pyaz_utils import call_az
from . import prefix


def delete(name, resource_group):
    '''
    Delete a public IP address.
    '''
    return call_az("az network public-ip delete", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a public IP address.
    '''
    return call_az("az network public-ip show", locals())


def list(resource_group=None):
    '''
    List public IP addresses.
    '''
    return call_az("az network public-ip list", locals())


def create(name, resource_group, allocation_method=None, dns_name=None, edge_zone=None, idle_timeout=None, ip_address=None, ip_tags=None, location=None, public_ip_prefix=None, reverse_fqdn=None, sku=None, tags=None, tier=None, version=None, zone=None):
    '''
    Create a public IP address.
    '''
    return call_az("az network public-ip create", locals())


def update(name, resource_group, add=None, allocation_method=None, dns_name=None, force_string=None, idle_timeout=None, ip_tags=None, public_ip_prefix=None, remove=None, reverse_fqdn=None, set=None, sku=None, tags=None, version=None):
    '''
    Update a public IP address.
    '''
    return call_az("az network public-ip update", locals())

