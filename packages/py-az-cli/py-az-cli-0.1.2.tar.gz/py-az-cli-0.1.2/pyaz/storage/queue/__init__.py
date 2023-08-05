from ... pyaz_utils import call_az
from . import metadata, policy


def create(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, fail_on_exist=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage queue create", locals())


def delete(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, fail_not_exist=None, sas_token=None, timeout=None):
    return call_az("az storage queue delete", locals())


def generate_sas(name, account_key=None, account_name=None, connection_string=None, expiry=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None):
    return call_az("az storage queue generate-sas", locals())


def stats(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage queue stats", locals())


def exists(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage queue exists", locals())


def list(account_key=None, account_name=None, auth_mode=None, connection_string=None, include_metadata=None, marker=None, num_results=None, prefix=None, sas_token=None, show_next_marker=None, timeout=None):
    '''
    List queues in a storage account.
    '''
    return call_az("az storage queue list", locals())

