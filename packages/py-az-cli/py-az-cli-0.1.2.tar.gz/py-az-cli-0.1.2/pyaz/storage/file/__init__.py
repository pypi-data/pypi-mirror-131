from ... pyaz_utils import call_az
from . import copy, metadata


def list(share_name, account_key=None, account_name=None, connection_string=None, exclude_dir=None, marker=None, num_results=None, path=None, sas_token=None, snapshot=None, timeout=None):
    '''
    List files and directories in a share.
    '''
    return call_az("az storage file list", locals())


def delete(path, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage file delete", locals())


def resize(path, share_name, size, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage file resize", locals())


def url(path, share_name, account_key=None, account_name=None, connection_string=None, protocol=None, sas_token=None):
    '''
    Create the url to access a file.
    '''
    return call_az("az storage file url", locals())


def generate_sas(path, share_name, account_key=None, account_name=None, cache_control=None, connection_string=None, content_disposition=None, content_encoding=None, content_language=None, content_type=None, expiry=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    return call_az("az storage file generate-sas", locals())


def show(path, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage file show", locals())


def update(path, share_name, account_key=None, account_name=None, clear_content_settings=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, sas_token=None, timeout=None):
    return call_az("az storage file update", locals())


def exists(path, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Check for the existence of a file.
    '''
    return call_az("az storage file exists", locals())


def download(path, share_name, account_key=None, account_name=None, connection_string=None, dest=None, end_range=None, max_connections=None, no_progress=None, open_mode=None, sas_token=None, snapshot=None, start_range=None, timeout=None, validate_content=None):
    return call_az("az storage file download", locals())


def upload(share_name, source, account_key=None, account_name=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, max_connections=None, metadata=None, no_progress=None, path=None, sas_token=None, timeout=None, validate_content=None):
    '''
    Upload a file to a share that uses the SMB 3.0 protocol.
    '''
    return call_az("az storage file upload", locals())


def upload_batch(destination, source, account_key=None, account_name=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, destination_path=None, dryrun=None, max_connections=None, metadata=None, no_progress=None, pattern=None, sas_token=None, validate_content=None):
    '''
    Upload files from a local directory to an Azure Storage File Share in a batch operation.
    '''
    return call_az("az storage file upload-batch", locals())


def download_batch(destination, source, account_key=None, account_name=None, connection_string=None, dryrun=None, max_connections=None, no_progress=None, pattern=None, sas_token=None, snapshot=None, validate_content=None):
    '''
    Download files from an Azure Storage File Share to a local directory in a batch operation.
    '''
    return call_az("az storage file download-batch", locals())


def delete_batch(source, account_key=None, account_name=None, connection_string=None, dryrun=None, pattern=None, sas_token=None, timeout=None):
    '''
    Delete files from an Azure Storage File Share.
    '''
    return call_az("az storage file delete-batch", locals())

