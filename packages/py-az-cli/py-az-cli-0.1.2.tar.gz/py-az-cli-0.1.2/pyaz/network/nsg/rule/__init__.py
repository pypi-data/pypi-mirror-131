from .... pyaz_utils import call_az

def delete(name, nsg_name, resource_group):
    '''
    Delete a network security group rule.
    '''
    return call_az("az network nsg rule delete", locals())


def list(nsg_name, resource_group, include_default=None):
    '''
    List all rules in a network security group.
    '''
    return call_az("az network nsg rule list", locals())


def show(name, nsg_name, resource_group):
    '''
    Get the details of a network security group rule.
    '''
    return call_az("az network nsg rule show", locals())


def create(name, nsg_name, priority, resource_group, access=None, description=None, destination_address_prefixes=None, destination_asgs=None, destination_port_ranges=None, direction=None, protocol=None, source_address_prefixes=None, source_asgs=None, source_port_ranges=None):
    '''
    Create a network security group rule.
    '''
    return call_az("az network nsg rule create", locals())


def update(name, nsg_name, resource_group, access=None, add=None, description=None, destination_address_prefixes=None, destination_asgs=None, destination_port_ranges=None, direction=None, force_string=None, priority=None, protocol=None, remove=None, set=None, source_address_prefixes=None, source_asgs=None, source_port_ranges=None):
    '''
    Update a network security group rule.
    '''
    return call_az("az network nsg rule update", locals())

