from .... pyaz_utils import call_az

def create(gateway_name, name, public_cert_data, resource_group):
    '''
    Upload a root certificate.
    '''
    return call_az("az network vnet-gateway root-cert create", locals())


def delete(gateway_name, name, resource_group):
    '''
    Delete a root certificate.
    '''
    return call_az("az network vnet-gateway root-cert delete", locals())

