from .... pyaz_utils import call_az

def create(name, share_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage share policy create", locals())


def delete(name, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage share policy delete", locals())


def show(name, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage share policy show", locals())


def list(share_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage share policy list", locals())


def update(name, share_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage share policy update", locals())

