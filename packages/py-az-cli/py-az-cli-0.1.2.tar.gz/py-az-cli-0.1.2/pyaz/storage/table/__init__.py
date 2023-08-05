from ... pyaz_utils import call_az
from . import policy


def create(name, account_key=None, account_name=None, connection_string=None, fail_on_exist=None, sas_token=None, timeout=None):
    return call_az("az storage table create", locals())


def delete(name, account_key=None, account_name=None, connection_string=None, fail_not_exist=None, sas_token=None, timeout=None):
    return call_az("az storage table delete", locals())


def exists(name, account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage table exists", locals())


def generate_sas(name, account_key=None, account_name=None, connection_string=None, end_pk=None, end_rk=None, expiry=None, https_only=None, ip=None, permissions=None, policy_name=None, start=None, start_pk=None, start_rk=None):
    return call_az("az storage table generate-sas", locals())


def list(account_key=None, account_name=None, connection_string=None, marker=None, num_results=None, sas_token=None, timeout=None):
    '''
    List tables in a storage account.
    '''
    return call_az("az storage table list", locals())


def stats(account_key=None, account_name=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage table stats", locals())

