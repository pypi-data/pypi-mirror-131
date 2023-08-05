from .... pyaz_utils import call_az

def upload(certificate_file, certificate_password, name, resource_group, slot=None):
    '''
    Upload an SSL certificate to a web app.
    '''
    return call_az("az webapp config ssl upload", locals())


def list(resource_group):
    '''
    List SSL certificates for a web app.
    '''
    return call_az("az webapp config ssl list", locals())


def show(certificate_name, resource_group):
    '''
    Show the details of an SSL certificate for a web app.
    '''
    return call_az("az webapp config ssl show", locals())


def bind(certificate_thumbprint, name, resource_group, ssl_type, slot=None):
    '''
    Bind an SSL certificate to a web app.
    '''
    return call_az("az webapp config ssl bind", locals())


def unbind(certificate_thumbprint, name, resource_group, slot=None):
    '''
    Unbind an SSL certificate from a web app.
    '''
    return call_az("az webapp config ssl unbind", locals())


def delete(certificate_thumbprint, resource_group):
    '''
    Delete an SSL certificate from a web app.
    '''
    return call_az("az webapp config ssl delete", locals())


def import_(key_vault, key_vault_certificate_name, name, resource_group):
    '''
    Import an SSL or App Service Certificate to a web app from Key Vault.
    '''
    return call_az("az webapp config ssl import", locals())


def create(hostname, name, resource_group, slot=None):
    '''
    Create a Managed Certificate for a hostname in a webapp app.
    '''
    return call_az("az webapp config ssl create", locals())

