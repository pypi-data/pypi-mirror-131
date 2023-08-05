from ... pyaz_utils import call_az

def list(resource_group=None):
    '''
    List app service environments.
    '''
    return call_az("az appservice ase list", locals())


def list_addresses(name, resource_group=None):
    '''
    List VIPs associated with an app service environment v2.
    '''
    return call_az("az appservice ase list-addresses", locals())


def list_plans(name, resource_group=None):
    '''
    List app service plans associated with an app service environment.
    '''
    return call_az("az appservice ase list-plans", locals())


def show(name, resource_group=None):
    '''
    Show details of an app service environment.
    '''
    return call_az("az appservice ase show", locals())


def create(name, resource_group, subnet, force_network_security_group=None, force_route_table=None, front_end_scale_factor=None, front_end_sku=None, ignore_network_security_group=None, ignore_route_table=None, ignore_subnet_size_validation=None, kind=None, location=None, no_wait=None, os_preference=None, virtual_ip_type=None, vnet_name=None, zone_redundant=None):
    '''
    Create app service environment.
    '''
    return call_az("az appservice ase create", locals())


def update(name, allow_new_private_endpoint_connections=None, front_end_scale_factor=None, front_end_sku=None, no_wait=None, resource_group=None):
    '''
    Update app service environment.
    '''
    return call_az("az appservice ase update", locals())


def delete(name, no_wait=None, resource_group=None, yes=None):
    '''
    Delete app service environment.
    '''
    return call_az("az appservice ase delete", locals())


def create_inbound_services(name, resource_group, subnet, skip_dns=None, vnet_name=None):
    '''
    Private DNS Zone for Internal ASEv2.
    '''
    return call_az("az appservice ase create-inbound-services", locals())

