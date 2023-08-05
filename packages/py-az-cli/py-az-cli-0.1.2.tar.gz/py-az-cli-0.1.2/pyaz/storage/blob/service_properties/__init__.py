from .... pyaz_utils import call_az
from . import delete_policy


def show(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage blob service-properties show", locals())


def update(404_document=None, account_key=None, account_name=None, add=None, auth_mode=None, connection_string=None, delete_retention=None, delete_retention_period=None, force_string=None, index_document=None, remove=None, sas_token=None, set=None, static_website=None, timeout=None):
    '''
    Update storage blob service properties.
    '''
    return call_az("az storage blob service-properties update", locals())

