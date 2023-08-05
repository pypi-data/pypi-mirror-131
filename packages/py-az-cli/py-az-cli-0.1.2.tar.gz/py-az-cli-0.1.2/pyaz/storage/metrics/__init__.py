from ... pyaz_utils import call_az

def update(retention, services, account_key=None, account_name=None, api=None, connection_string=None, hour=None, minute=None, sas_token=None, timeout=None):
    '''
    Update metrics settings for a storage account.
    '''
    return call_az("az storage metrics update", locals())


def show(account_key=None, account_name=None, connection_string=None, interval=None, sas_token=None, services=None, timeout=None):
    '''
    Show metrics settings for a storage account.
    '''
    return call_az("az storage metrics show", locals())

