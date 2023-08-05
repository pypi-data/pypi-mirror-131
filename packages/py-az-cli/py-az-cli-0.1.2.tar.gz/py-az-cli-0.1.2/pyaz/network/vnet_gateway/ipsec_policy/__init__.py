from .... pyaz_utils import call_az

def add(dh_group, gateway_name, ike_encryption, ike_integrity, ipsec_encryption, ipsec_integrity, pfs_group, resource_group, sa_lifetime, sa_max_size, no_wait=None):
    '''
    Add a virtual network gateway IPSec policy.
    '''
    return call_az("az network vnet-gateway ipsec-policy add", locals())


def list(gateway_name, resource_group):
    '''
    List IPSec policies associated with a virtual network gateway.
    '''
    return call_az("az network vnet-gateway ipsec-policy list", locals())


def clear(gateway_name, resource_group, no_wait=None):
    '''
    Delete all IPsec policies on a virtual network gateway.
    '''
    return call_az("az network vnet-gateway ipsec-policy clear", locals())

