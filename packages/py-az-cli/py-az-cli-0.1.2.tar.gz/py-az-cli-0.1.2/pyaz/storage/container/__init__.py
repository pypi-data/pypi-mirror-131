from ... pyaz_utils import call_az
from . import immutability_policy, lease, legal_hold, metadata, policy


def list(account_key=None, account_name=None, auth_mode=None, connection_string=None, include_deleted=None, include_metadata=None, marker=None, num_results=None, prefix=None, sas_token=None, show_next_marker=None, timeout=None):
    '''
    List containers in a storage account.
    '''
    return call_az("az storage container list", locals())


def delete(name, account_key=None, account_name=None, auth_mode=None, bypass_immutability_policy=None, connection_string=None, fail_not_exist=None, if_modified_since=None, if_unmodified_since=None, lease_id=None, sas_token=None, timeout=None):
    '''
    Marks the specified container for deletion.
    '''
    return call_az("az storage container delete", locals())


def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage container show", locals())


def create(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, default_encryption_scope=None, fail_on_exist=None, metadata=None, prevent_encryption_scope_override=None, public_access=None, resource_group=None, sas_token=None, timeout=None):
    '''
    Create a container in a storage account.
    '''
    return call_az("az storage container create", locals())


def generate_sas(name, account_key=None, account_name=None, as_user=None, auth_mode=None, cache_control=None, connection_string=None, content_disposition=None, content_encoding=None, content_language=None, content_type=None, expiry=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    '''
    Generate a SAS token for a storage container.
    '''
    return call_az("az storage container generate-sas", locals())


def exists(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Check for the existence of a storage container.
    '''
    return call_az("az storage container exists", locals())


def set_permission(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, lease_id=None, public_access=None, sas_token=None, timeout=None):
    return call_az("az storage container set-permission", locals())


def show_permission(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage container show-permission", locals())


def restore(deleted_version, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Restore soft-deleted container.
    '''
    return call_az("az storage container restore", locals())

