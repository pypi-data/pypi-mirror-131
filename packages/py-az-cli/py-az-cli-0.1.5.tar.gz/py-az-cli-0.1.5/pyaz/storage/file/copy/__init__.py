from .... pyaz_utils import _call_az

def start(destination_path, destination_share, account_key=None, account_name=None, connection_string=None, file_snapshot=None, metadata=None, sas_token=None, source_account_key=None, source_account_name=None, source_blob=None, source_container=None, source_path=None, source_sas=None, source_share=None, source_snapshot=None, source_uri=None, timeout=None):
    '''
    Copy a file asynchronously.
    '''
    return _call_az("az storage file copy start", locals())


def cancel(copy_id, destination_path, destination_share, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return _call_az("az storage file copy cancel", locals())


def start_batch(account_key=None, account_name=None, connection_string=None, destination_path=None, destination_share=None, dryrun=None, metadata=None, pattern=None, sas_token=None, source_account_key=None, source_account_name=None, source_client=None, source_container=None, source_sas=None, source_share=None, source_uri=None, timeout=None):
    '''
    Copy multiple files or blobs to a file share.
    '''
    return _call_az("az storage file copy start-batch", locals())

