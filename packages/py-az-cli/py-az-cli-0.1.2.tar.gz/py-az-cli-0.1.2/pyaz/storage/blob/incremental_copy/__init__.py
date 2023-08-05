from .... pyaz_utils import call_az

def start(destination_blob, destination_container, account_key=None, account_name=None, auth_mode=None, connection_string=None, destination_if_match=None, destination_if_modified_since=None, destination_if_none_match=None, destination_if_unmodified_since=None, destination_lease_id=None, metadata=None, sas_token=None, source_account_key=None, source_account_name=None, source_blob=None, source_container=None, source_lease_id=None, source_sas=None, source_snapshot=None, source_uri=None, timeout=None):
    '''
    Copies an incremental copy of a blob asynchronously.
    '''
    return call_az("az storage blob incremental-copy start", locals())


def cancel(container_name, copy_id, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage blob incremental-copy cancel", locals())

