from .... pyaz_utils import call_az

def create(name, table_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage table policy create", locals())


def delete(name, table_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage table policy delete", locals())


def show(name, table_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage table policy show", locals())


def list(table_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage table policy list", locals())


def update(name, table_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage table policy update", locals())

