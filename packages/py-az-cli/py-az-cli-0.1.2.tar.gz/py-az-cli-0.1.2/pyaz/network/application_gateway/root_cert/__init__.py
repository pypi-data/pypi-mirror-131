from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List trusted root certificates.
    '''
    return call_az("az network application-gateway root-cert list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a trusted root certificate.
    '''
    return call_az("az network application-gateway root-cert show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a trusted root certificate.
    '''
    return call_az("az network application-gateway root-cert delete", locals())


def create(gateway_name, name, resource_group, cert_file=None, keyvault_secret=None, no_wait=None):
    '''
    Upload a trusted root certificate.
    '''
    return call_az("az network application-gateway root-cert create", locals())


def update(gateway_name, name, resource_group, add=None, cert_file=None, force_string=None, keyvault_secret=None, no_wait=None, remove=None, set=None):
    '''
    Update a trusted root certificate.
    '''
    return call_az("az network application-gateway root-cert update", locals())

