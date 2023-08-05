from .... pyaz_utils import call_az
from . import metadata


def create(account_key=None, account_name=None, auth_mode=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, metadata=None, permissions=None, sas_token=None, timeout=None, umask=None):
    '''
    Create a new file in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file create", locals())


def upload(source, account_key=None, account_name=None, auth_mode=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, metadata=None, overwrite=None, permissions=None, sas_token=None, timeout=None, umask=None):
    '''
    Upload a file to a file path in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file upload", locals())


def exists(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Check for the existence of a file in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file exists", locals())


def append(content, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Append content to a file in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file append", locals())


def download(account_key=None, account_name=None, auth_mode=None, connection_string=None, destination=None, overwrite=None, sas_token=None, timeout=None):
    '''
    Download a file from the specified path in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file download", locals())


def show(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Show properties of file in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file show", locals())


def list(account_key=None, account_name=None, auth_mode=None, connection_string=None, exclude_dir=None, marker=None, num_results=None, path=None, recursive=None, sas_token=None, show_next_marker=None, timeout=None):
    '''
    List files and directories in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file list", locals())


def move(new_path, account_key=None, account_name=None, auth_mode=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, sas_token=None):
    '''
    Move a file in ADLS Gen2 Account.
    '''
    return call_az("az storage fs file move", locals())


def delete(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None, yes=None):
    '''
    Delete a file in ADLS Gen2 file system.
    '''
    return call_az("az storage fs file delete", locals())

