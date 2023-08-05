from .... pyaz_utils import call_az

def start(destination_blob, destination_container, account_key=None, account_name=None, auth_mode=None, connection_string=None, destination_if_match=None, destination_if_modified_since=None, destination_if_none_match=None, destination_if_unmodified_since=None, destination_lease_id=None, destination_tags_condition=None, metadata=None, rehydrate_priority=None, requires_sync=None, sas_token=None, source_account_key=None, source_account_name=None, source_blob=None, source_container=None, source_if_match=None, source_if_modified_since=None, source_if_none_match=None, source_if_unmodified_since=None, source_lease_id=None, source_path=None, source_sas=None, source_share=None, source_snapshot=None, source_tags_condition=None, source_uri=None, tags=None, tier=None, timeout=None):
    '''
    Copy a blob asynchronously. Use `az storage blob show` to check the status of the blobs.
    '''
    return call_az("az storage blob copy start", locals())


def cancel(copy_id, destination_blob, destination_container, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage blob copy cancel", locals())


def start_batch(account_key=None, account_name=None, auth_mode=None, connection_string=None, destination_container=None, destination_path=None, dryrun=None, pattern=None, sas_token=None, source_account_key=None, source_account_name=None, source_client=None, source_container=None, source_sas=None, source_share=None, source_uri=None):
    '''
    Copy multiple blobs to a blob container. Use `az storage blob show` to check the status of the blobs.
    '''
    return call_az("az storage blob copy start-batch", locals())

