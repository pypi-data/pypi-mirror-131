from .... pyaz_utils import call_az
from . import metadata


def create(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, metadata=None, permissions=None, sas_token=None, timeout=None, umask=None):
    '''
    Create a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory create", locals())


def exists(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Check for the existence of a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory exists", locals())


def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Show properties of a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory show", locals())


def delete(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None, yes=None):
    '''
    Delete a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory delete", locals())


def move(name, new_directory, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Move a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory move", locals())


def list(account_key=None, account_name=None, auth_mode=None, connection_string=None, num_results=None, path=None, recursive=None, sas_token=None, timeout=None):
    '''
    List directories in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory list", locals())


def upload(file_system, source, account_key=None, account_name=None, auth_mode=None, connection_string=None, destination_path=None, recursive=None, sas_token=None):
    '''
    Upload files or subdirectories to a directory in ADLS Gen2 file system.
    '''
    return call_az("az storage fs directory upload", locals())


def download(destination_path, file_system, account_key=None, account_name=None, auth_mode=None, connection_string=None, recursive=None, sas_token=None, source_path=None):
    '''
    Download files from the directory in ADLS Gen2 file system to a local file path.
    '''
    return call_az("az storage fs directory download", locals())

