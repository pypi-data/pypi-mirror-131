from .... pyaz_utils import call_az

def update(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, if_modified_since=None, lease_id=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage container metadata update", locals())


def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None, timeout=None):
    return call_az("az storage container metadata show", locals())

