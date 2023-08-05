from .. pyaz_utils import call_az
from . import account, container, container_rm, cors, directory, entity, file, fs, logging, message, metrics, queue, share, share_rm, table


def remove(account_key=None, account_name=None, connection_string=None, container_name=None, exclude_path=None, exclude_pattern=None, include_path=None, include_pattern=None, name=None, path=None, recursive=None, sas_token=None, share_name=None):
    '''
    Delete blobs or files from Azure Storage.
    '''
    return call_az("az storage remove", locals())


def copy(account_key=None, account_name=None, blob_type=None, cap_mbps=None, connection_string=None, content_type=None, destination=None, destination_blob=None, destination_container=None, destination_file_path=None, destination_share=None, exclude_path=None, exclude_pattern=None, follow_symlinks=None, include_path=None, include_pattern=None, preserve_s2s_access_tier=None, put_md5=None, recursive=None, sas_token=None, source=None, source_account_key=None, source_account_name=None, source_blob=None, source_connection_string=None, source_container=None, source_file_path=None, source_sas=None, source_share=None):
    '''
    Copy files or directories to or from Azure storage.
    '''
    return call_az("az storage copy", locals())

