from ... pyaz_utils import call_az

def list(name, resource_group=None):
    '''
    List custom hostnames of the static app.
    '''
    return call_az("az staticwebapp hostname list", locals())


def set(hostname, name, no_wait=None, resource_group=None, validation_method=None):
    '''
    Set given sub-domain hostname to the static app. Please configure CNAME/TXT/ALIAS record with your DNS provider. Use --no-wait to not wait for validation.
    '''
    return call_az("az staticwebapp hostname set", locals())


def delete(hostname, name, no_wait=None, resource_group=None, yes=None):
    '''
    Delete given hostname of the static app.
    '''
    return call_az("az staticwebapp hostname delete", locals())


def show(hostname, name, resource_group):
    '''
    Get details for a staticwebapp custom domain. Can be used to fetch validation token for TXT domain validation (see example).
    '''
    return call_az("az staticwebapp hostname show", locals())

