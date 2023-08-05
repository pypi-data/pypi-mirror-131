from .... pyaz_utils import call_az

def show(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage blob metadata show", locals())


def update(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, lease_id=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage blob metadata update", locals())

