from ... pyaz_utils import call_az
from . import metadata, policy


def list(account_key=None, account_name=None, connection_string=None, include_metadata=None, include_snapshots=None, marker=None, num_results=None, prefix=None, sas_token=None, timeout=None):
    '''
    List the file shares in a storage account.
    '''
    return call_az("az storage share list", locals())


def create(name, account_key=None, account_name=None, connection_string=None, fail_on_exist=None, metadata=None, quota=None, sas_token=None, timeout=None):
    '''
    Creates a new share under the specified account.
    '''
    return call_az("az storage share create", locals())


def delete(name, account_key=None, account_name=None, connection_string=None, delete_snapshots=None, fail_not_exist=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage share delete", locals())


def generate_sas(name, account_key=None, account_name=None, cache_control=None, connection_string=None, content_disposition=None, content_encoding=None, content_language=None, content_type=None, expiry=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    return call_az("az storage share generate-sas", locals())


def stats(name, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage share stats", locals())


def show(name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage share show", locals())


def update(name, quota, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage share update", locals())


def snapshot(name, account_key=None, account_name=None, connection_string=None, metadata=None, quota=None, sas_token=None, timeout=None):
    return call_az("az storage share snapshot", locals())


def exists(name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Check for the existence of a file share.
    '''
    return call_az("az storage share exists", locals())


def url(name, account_key=None, account_name=None, connection_string=None, protocol=None, sas_token=None, unc=None):
    '''
    Create a URI to access a file share.
    '''
    return call_az("az storage share url", locals())


def list_handle(name, account_key=None, account_name=None, connection_string=None, marker=None, max_results=None, path=None, recursive=None, sas_token=None, snapshot=None, timeout=None):
    '''
    List file handles of a file share.
    '''
    return call_az("az storage share list-handle", locals())


def close_handle(name, account_key=None, account_name=None, close_all=None, connection_string=None, handle_id=None, marker=None, path=None, recursive=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Close file handles of a file share.
    '''
    return call_az("az storage share close-handle", locals())

