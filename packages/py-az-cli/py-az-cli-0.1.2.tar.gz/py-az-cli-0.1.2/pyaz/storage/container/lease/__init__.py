from .... pyaz_utils import call_az

def acquire(container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, lease_duration=None, proposed_lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage container lease acquire", locals())


def renew(container_name, lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, sas_token=None, timeout=None):
    return call_az("az storage container lease renew", locals())


def release(container_name, lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, sas_token=None, timeout=None):
    return call_az("az storage container lease release", locals())


def change(container_name, lease_id, proposed_lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, sas_token=None, timeout=None):
    return call_az("az storage container lease change", locals())


def break_(container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, if_unmodified_since=None, lease_break_period=None, sas_token=None, timeout=None):
    return call_az("az storage container lease break", locals())

