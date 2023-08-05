from .... pyaz_utils import call_az

def assign(audience, gateway_name, issuer, resource_group, tenant, no_wait=None):
    '''
    Assign/Update AAD(Azure Active Directory) authentication to a virtual network gateway.
    '''
    return call_az("az network vnet-gateway aad assign", locals())


def show(gateway_name, resource_group):
    '''
    Show AAD(Azure Active Directory) authentication of a virtual network gateway
    '''
    return call_az("az network vnet-gateway aad show", locals())


def remove(gateway_name, resource_group, no_wait=None):
    '''
    Remove AAD(Azure Active Directory) authentication from a virtual network gateway
    '''
    return call_az("az network vnet-gateway aad remove", locals())

