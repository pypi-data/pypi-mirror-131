from .... pyaz_utils import call_az

def create(name, remote_vnet, resource_group, vnet_name, allow_forwarded_traffic=None, allow_gateway_transit=None, allow_vnet_access=None, use_remote_gateways=None):
    '''
    Create a virtual network peering connection.
    '''
    return call_az("az network vnet peering create", locals())


def show(name, resource_group, vnet_name):
    '''
    Show details of a peering.
    '''
    return call_az("az network vnet peering show", locals())


def list(resource_group, vnet_name):
    '''
    List peerings.
    '''
    return call_az("az network vnet peering list", locals())


def delete(name, resource_group, vnet_name):
    '''
    Delete a peering.
    '''
    return call_az("az network vnet peering delete", locals())


def update(name, resource_group, vnet_name, add=None, force_string=None, remove=None, set=None):
    '''
    Update a peering.
    '''
    return call_az("az network vnet peering update", locals())

