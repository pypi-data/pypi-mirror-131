from .... pyaz_utils import call_az

def create(name, peer_asn, peer_ip, resource_group, vrouter_name):
    '''
    Create a virtual router peering.
    '''
    return call_az("az network vrouter peering create", locals())


def update(name, resource_group, vrouter_name, add=None, force_string=None, peer_asn=None, peer_ip=None, remove=None, set=None):
    '''
    Update a virtual router peering.
    '''
    return call_az("az network vrouter peering update", locals())


def delete(name, resource_group, vrouter_name):
    '''
    Delete a virtual router peering.
    '''
    return call_az("az network vrouter peering delete", locals())


def show(name, resource_group, vrouter_name):
    '''
    Show a virtual router peering
    '''
    return call_az("az network vrouter peering show", locals())


def list(resource_group, vrouter_name):
    '''
    List all virtual router peerings under a resource group.
    '''
    return call_az("az network vrouter peering list", locals())

