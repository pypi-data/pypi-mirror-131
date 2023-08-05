from .... pyaz_utils import call_az

def acquire(blob_name, container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_duration=None, proposed_lease_id=None, sas_token=None, tags_condition=None, timeout=None):
    '''
    Request a new lease.
    '''
    return call_az("az storage blob lease acquire", locals())


def break_(blob_name, container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_break_period=None, sas_token=None, tags_condition=None, timeout=None):
    return call_az("az storage blob lease break", locals())


def change(blob_name, container_name, lease_id, proposed_lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, sas_token=None, tags_condition=None, timeout=None):
    return call_az("az storage blob lease change", locals())


def renew(blob_name, container_name, lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, sas_token=None, tags_condition=None, timeout=None):
    '''
    Renew the lease.
    '''
    return call_az("az storage blob lease renew", locals())


def release(blob_name, container_name, lease_id, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, sas_token=None, tags_condition=None, timeout=None):
    return call_az("az storage blob lease release", locals())

