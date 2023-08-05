from ... pyaz_utils import call_az
from . import access, directory, file, metadata


def create(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, metadata=None, public_access=None, sas_token=None, timeout=None):
    '''
    Create file system for Azure Data Lake Storage Gen2 account.
    '''
    return call_az("az storage fs create", locals())


def list(account_key=None, account_name=None, auth_mode=None, connection_string=None, include_metadata=None, prefix=None, sas_token=None):
    '''
    List file systems in ADLS Gen2 account.
    '''
    return call_az("az storage fs list", locals())


def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Show properties of file system in ADLS Gen2 account.
    '''
    return call_az("az storage fs show", locals())


def delete(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None, yes=None):
    '''
    Delete a file system in ADLS Gen2 account.
    '''
    return call_az("az storage fs delete", locals())


def exists(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Check for the existence of a file system in ADLS Gen2 account.
    '''
    return call_az("az storage fs exists", locals())


def generate_sas(name, account_key=None, account_name=None, as_user=None, auth_mode=None, cache_control=None, connection_string=None, content_disposition=None, content_encoding=None, content_language=None, content_type=None, expiry=None, full_uri=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    '''
    Generate a SAS token for file system in ADLS Gen2 account.
    '''
    return call_az("az storage fs generate-sas", locals())

