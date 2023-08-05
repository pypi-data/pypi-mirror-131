from ..... pyaz_utils import call_az

def set(dh_group, ike_encryption, ike_integrity, ipsec_encryption, ipsec_integrity, name, pfs_group, resource_group, sa_lifetime, sa_max_size, no_wait=None):
    '''
    Set the VPN client connection ipsec policy per P2S client connection of the virtual network gateway.
    '''
    return call_az("az network vnet-gateway vpn-client ipsec-policy set", locals())


def show(name, resource_group):
    '''
    Get the VPN client connection ipsec policy per P2S client connection of the virtual network gateway.
    '''
    return call_az("az network vnet-gateway vpn-client ipsec-policy show", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the vnet gateway vpn client ipsec policy is met.
    '''
    return call_az("az network vnet-gateway vpn-client ipsec-policy wait", locals())

