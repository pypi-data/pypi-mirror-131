from .... pyaz_utils import call_az

def add(connection_name, dh_group, ike_encryption, ike_integrity, ipsec_encryption, ipsec_integrity, pfs_group, resource_group, sa_lifetime, sa_max_size, no_wait=None):
    '''
    Add a VPN connection IPSec policy.
    '''
    return call_az("az network vpn-connection ipsec-policy add", locals())


def list(connection_name, resource_group):
    '''
    List IPSec policies associated with a VPN connection.
    '''
    return call_az("az network vpn-connection ipsec-policy list", locals())


def clear(connection_name, resource_group, no_wait=None):
    '''
    Delete all IPsec policies on a VPN connection.
    '''
    return call_az("az network vpn-connection ipsec-policy clear", locals())

