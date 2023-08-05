from ... pyaz_utils import call_az
from . import connection


def create(lb_frontend_ip_configs, name, resource_group, subnet, auto_approval=None, edge_zone=None, enable_proxy_protocol=None, fqdns=None, lb_name=None, location=None, private_ip_address=None, private_ip_address_version=None, private_ip_allocation_method=None, public_ip_address=None, tags=None, visibility=None, vnet_name=None):
    '''
    Create a private link service.
    '''
    return call_az("az network private-link-service create", locals())


def delete(name, resource_group):
    '''
    Delete a private link service.
    '''
    return call_az("az network private-link-service delete", locals())


def list(resource_group=None):
    '''
    List private link services.
    '''
    return call_az("az network private-link-service list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a private link service.
    '''
    return call_az("az network private-link-service show", locals())


def update(name, resource_group, add=None, auto_approval=None, enable_proxy_protocol=None, force_string=None, fqdns=None, lb_frontend_ip_configs=None, lb_name=None, remove=None, set=None, tags=None, visibility=None):
    '''
    Update a private link service.
    '''
    return call_az("az network private-link-service update", locals())

