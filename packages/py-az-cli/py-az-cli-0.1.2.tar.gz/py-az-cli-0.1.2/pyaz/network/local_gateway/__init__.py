from ... pyaz_utils import call_az

def delete(name, resource_group, no_wait=None):
    '''
    Delete a local VPN gateway.
    '''
    return call_az("az network local-gateway delete", locals())


def show(name, resource_group):
    '''
    Get the details of a local VPN gateway.
    '''
    return call_az("az network local-gateway show", locals())


def list(resource_group):
    '''
    List all local VPN gateways in a resource group.
    '''
    return call_az("az network local-gateway list", locals())


def create(gateway_ip_address, name, resource_group, asn=None, bgp_peering_address=None, local_address_prefixes=None, location=None, no_wait=None, peer_weight=None, tags=None):
    '''
    Create a local VPN gateway.
    '''
    return call_az("az network local-gateway create", locals())


def update(name, resource_group, add=None, asn=None, bgp_peering_address=None, force_string=None, gateway_ip_address=None, local_address_prefixes=None, no_wait=None, peer_weight=None, remove=None, set=None, tags=None):
    '''
    Update a local VPN gateway.
    '''
    return call_az("az network local-gateway update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the local gateway is met.
    '''
    return call_az("az network local-gateway wait", locals())

