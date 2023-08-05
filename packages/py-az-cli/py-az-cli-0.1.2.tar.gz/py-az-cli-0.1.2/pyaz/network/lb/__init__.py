from ... pyaz_utils import call_az
from . import address_pool, frontend_ip, inbound_nat_pool, inbound_nat_rule, outbound_rule, probe, rule


def show(name, resource_group, expand=None):
    '''
    Get the details of a load balancer.
    '''
    return call_az("az network lb show", locals())


def create(name, resource_group, backend_pool_name=None, edge_zone=None, frontend_ip_name=None, frontend_ip_zone=None, location=None, no_wait=None, private_ip_address=None, private_ip_address_version=None, public_ip_address=None, public_ip_address_allocation=None, public_ip_dns_name=None, public_ip_zone=None, sku=None, subnet=None, subnet_address_prefix=None, tags=None, validate=None, vnet_address_prefix=None, vnet_name=None):
    '''
    Create a load balancer.
    '''
    return call_az("az network lb create", locals())


def delete(name, resource_group):
    '''
    Delete a load balancer.
    '''
    return call_az("az network lb delete", locals())


def list(resource_group=None):
    '''
    List load balancers.
    '''
    return call_az("az network lb list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the load balancer is met.
    '''
    return call_az("az network lb wait", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a load balancer.
    '''
    return call_az("az network lb update", locals())


def list_nic(name, resource_group):
    '''
    List associated load balancer network interfaces.
    '''
    return call_az("az network lb list-nic", locals())

