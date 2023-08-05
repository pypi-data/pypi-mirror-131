from .... pyaz_utils import call_az

def grant(api, id, consent_type=None, expires=None, principal_id=None, scope=None):
    '''
    Grant the app an API Delegated permissions
    '''
    return call_az("az ad app permission grant", locals())


def list(id):
    '''
    List API permissions the application has requested
    '''
    return call_az("az ad app permission list", locals())


def add(api, api_permissions, id):
    '''
    Add an API permission
    '''
    return call_az("az ad app permission add", locals())


def delete(api, id, api_permissions=None):
    '''
    Remove an API permission
    '''
    return call_az("az ad app permission delete", locals())


def list_grants(filter=None, id=None, show_resource_name=None):
    '''
    List Oauth2 permission grants
    '''
    return call_az("az ad app permission list-grants", locals())


def admin_consent(id):
    '''
    Grant Application & Delegated permissions through admin-consent.
    '''
    return call_az("az ad app permission admin-consent", locals())

