from ... pyaz_utils import call_az

def update(log, retention, services, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None, version=None):
    '''
    Update logging settings for a storage account.
    '''
    return call_az("az storage logging update", locals())


def show(account_key=None, account_name=None, connection_string=None, sas_token=None, services=None, timeout=None):
    '''
    Show logging settings for a storage account.
    '''
    return call_az("az storage logging show", locals())


def off(account_key=None, account_name=None, connection_string=None, sas_token=None, services=None, timeout=None):
    '''
    Turn off logging for a storage account.
    '''
    return call_az("az storage logging off", locals())

