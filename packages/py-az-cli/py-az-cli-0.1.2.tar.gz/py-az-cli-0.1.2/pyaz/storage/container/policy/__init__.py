from .... pyaz_utils import call_az

def create(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, expiry=None, lease_id=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage container policy create", locals())


def delete(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None):
    return call_az("az storage container policy delete", locals())


def update(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, expiry=None, lease_id=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage container policy update", locals())


def show(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None):
    return call_az("az storage container policy show", locals())


def list(container_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, lease_id=None, sas_token=None):
    return call_az("az storage container policy list", locals())

