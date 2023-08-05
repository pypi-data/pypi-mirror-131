from ..... pyaz_utils import call_az

def show(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Show the storage blob delete-policy.
    '''
    return call_az("az storage blob service-properties delete-policy show", locals())


def update(account_key=None, account_name=None, auth_mode=None, connection_string=None, days_retained=None, enable=None, sas_token=None):
    '''
    Update the storage blob delete-policy.
    '''
    return call_az("az storage blob service-properties delete-policy update", locals())

