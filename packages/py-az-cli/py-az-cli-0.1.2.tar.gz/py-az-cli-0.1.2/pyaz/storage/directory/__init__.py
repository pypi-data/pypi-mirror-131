from ... pyaz_utils import call_az
from . import metadata


def create(name, share_name, account_key=None, account_name=None, connection_string=None, fail_on_exist=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage directory create", locals())


def delete(name, share_name, account_key=None, account_name=None, connection_string=None, fail_not_exist=None, sas_token=None, timeout=None):
    return call_az("az storage directory delete", locals())


def show(name, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage directory show", locals())


def exists(name, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Check for the existence of a storage directory.
    '''
    return call_az("az storage directory exists", locals())


def list(share_name, account_key=None, account_name=None, connection_string=None, name=None, sas_token=None, timeout=None):
    '''
    List directories in a share.
    '''
    return call_az("az storage directory list", locals())

