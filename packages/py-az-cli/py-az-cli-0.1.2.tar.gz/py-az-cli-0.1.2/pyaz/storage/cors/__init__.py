from ... pyaz_utils import call_az

def add(methods, origins, services, account_key=None, account_name=None, allowed_headers=None, connection_string=None, exposed_headers=None, max_age=None, sas_token=None, timeout=None):
    '''
    Add a CORS rule to a storage account.
    '''
    return call_az("az storage cors add", locals())


def clear(services, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Remove all CORS rules from a storage account.
    '''
    return call_az("az storage cors clear", locals())


def list(account_key=None, account_name=None, connection_string=None, sas_token=None, services=None, timeout=None):
    '''
    List all CORS rules for a storage account.
    '''
    return call_az("az storage cors list", locals())

