from .... pyaz_utils import _call_az

def create(gateway_name, name, resource_group, thumbprint):
    '''
    Revoke a certificate.
    '''
    return _call_az("az network vnet-gateway revoked-cert create", locals())


def delete(gateway_name, name, resource_group):
    '''
    Delete a revoked certificate.
    '''
    return _call_az("az network vnet-gateway revoked-cert delete", locals())

