from .... pyaz_utils import call_az

def create(address_prefixes, name, resource_group, vnet_name, delegations=None, disable_private_endpoint_network_policies=None, disable_private_link_service_network_policies=None, nat_gateway=None, network_security_group=None, route_table=None, service_endpoint_policy=None, service_endpoints=None):
    '''
    Create a subnet and associate an existing NSG and route table.
    '''
    return call_az("az network vnet subnet create", locals())


def delete(name, resource_group, vnet_name):
    '''
    Delete a subnet.
    '''
    return call_az("az network vnet subnet delete", locals())


def show(name, resource_group, vnet_name, expand=None):
    '''
    Show details of a subnet.
    '''
    return call_az("az network vnet subnet show", locals())


def list(resource_group, vnet_name):
    '''
    List the subnets in a virtual network.
    '''
    return call_az("az network vnet subnet list", locals())


def update(name, resource_group, vnet_name, add=None, address_prefixes=None, delegations=None, disable_private_endpoint_network_policies=None, disable_private_link_service_network_policies=None, force_string=None, nat_gateway=None, network_security_group=None, remove=None, route_table=None, service_endpoint_policy=None, service_endpoints=None, set=None):
    '''
    Update a subnet.
    '''
    return call_az("az network vnet subnet update", locals())


def list_available_delegations(location=None, resource_group=None):
    '''
    List the services available for subnet delegation.
    '''
    return call_az("az network vnet subnet list-available-delegations", locals())

