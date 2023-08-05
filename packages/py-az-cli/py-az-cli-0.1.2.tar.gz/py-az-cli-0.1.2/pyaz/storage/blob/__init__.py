from ... pyaz_utils import call_az
from . import copy, immutability_policy, incremental_copy, lease, metadata


def show(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, sas_token=None, snapshot=None, tags_condition=None, timeout=None):
    '''
    Get the details of a blob.
    '''
    return call_az("az storage blob show", locals())


def set_tier(container_name, name, tier, account_key=None, account_name=None, auth_mode=None, connection_string=None, rehydrate_priority=None, sas_token=None, timeout=None, type=None):
    '''
    Set the block or page tiers on the blob.
    '''
    return call_az("az storage blob set-tier", locals())


def list(container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, delimiter=None, include=None, marker=None, num_results=None, prefix=None, sas_token=None, show_next_marker=None, timeout=None):
    '''
    List blobs in a given container.
    '''
    return call_az("az storage blob list", locals())


def query(container_name, name, query_expression, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, in_column_separator=None, in_escape_char=None, in_has_header=None, in_line_separator=None, in_quote_char=None, in_record_separator=None, input_format=None, lease_id=None, out_column_separator=None, out_escape_char=None, out_has_header=None, out_line_separator=None, out_quote_char=None, out_record_separator=None, output_format=None, result_file=None, sas_token=None, tags_condition=None, timeout=None):
    '''
    Enable users to select/project on blob or blob snapshot data by providing simple query expressions.
    '''
    return call_az("az storage blob query", locals())


def rewrite(container_name, name, source_uri, account_key=None, account_name=None, auth_mode=None, connection_string=None, encryption_scope=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, sas_token=None, tags_condition=None, tier=None, timeout=None):
    '''
    Create a new Block Blob where the content of the blob is read from a given URL.
    '''
    return call_az("az storage blob rewrite", locals())


def set_legal_hold(container_name, legal_hold, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Set blob legal hold.
    '''
    return call_az("az storage blob set-legal-hold", locals())


def download(container_name, file, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, end_range=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, max_connections=None, no_progress=None, open_mode=None, sas_token=None, snapshot=None, socket_timeout=None, start_range=None, timeout=None, validate_content=None):
    return call_az("az storage blob download", locals())


def generate_sas(container_name, name, account_key=None, account_name=None, as_user=None, auth_mode=None, cache_control=None, connection_string=None, content_disposition=None, content_encoding=None, content_language=None, content_type=None, expiry=None, full_uri=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    '''
    Generate a shared access signature for the blob.
    '''
    return call_az("az storage blob generate-sas", locals())


def url(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, protocol=None, sas_token=None, snapshot=None):
    '''
    Create the url to access a blob.
    '''
    return call_az("az storage blob url", locals())


def snapshot(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage blob snapshot", locals())


def update(container_name, name, account_key=None, account_name=None, auth_mode=None, clear_content_settings=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage blob update", locals())


def exists(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Check for the existence of a blob in a container.
    '''
    return call_az("az storage blob exists", locals())


def delete(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, delete_snapshots=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, sas_token=None, snapshot=None, timeout=None):
    '''
    Mark a blob or snapshot for deletion.
    '''
    return call_az("az storage blob delete", locals())


def undelete(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage blob undelete", locals())


def upload(container_name, file, account_key=None, account_name=None, auth_mode=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, encryption_scope=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, max_connections=None, maxsize_condition=None, metadata=None, name=None, no_progress=None, sas_token=None, socket_timeout=None, tier=None, timeout=None, type=None, validate_content=None):
    '''
    Upload a file to a storage blob.
    '''
    return call_az("az storage blob upload", locals())


def upload_batch(destination, source, account_key=None, account_name=None, auth_mode=None, connection_string=None, content_cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_md5=None, content_type=None, destination_path=None, dryrun=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, max_connections=None, maxsize_condition=None, metadata=None, no_progress=None, pattern=None, sas_token=None, socket_timeout=None, timeout=None, type=None, validate_content=None):
    '''
    Upload files from a local directory to a blob container.
    '''
    return call_az("az storage blob upload-batch", locals())


def download_batch(destination, source, account_key=None, account_name=None, auth_mode=None, connection_string=None, dryrun=None, max_connections=None, no_progress=None, pattern=None, sas_token=None, socket_timeout=None):
    '''
    Download blobs from a blob container recursively.
    '''
    return call_az("az storage blob download-batch", locals())


def delete_batch(source, account_key=None, account_name=None, auth_mode=None, connection_string=None, delete_snapshots=None, dryrun=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, pattern=None, sas_token=None, timeout=None):
    '''
    Delete blobs from a blob container recursively.
    '''
    return call_az("az storage blob delete-batch", locals())


def restore(account_name, time_to_restore, blob_range=None, no_wait=None, resource_group=None):
    '''
    Restore blobs in the specified blob ranges.
    '''
    return call_az("az storage blob restore", locals())


def sync(container, source, account_key=None, account_name=None, auth_mode=None, connection_string=None, destination=None, exclude_path=None, exclude_pattern=None, include_pattern=None, sas_token=None):
    '''
    Sync blobs recursively to a storage blob container.
    '''
    return call_az("az storage blob sync", locals())

