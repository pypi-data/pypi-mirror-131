from .... pyaz_utils import call_az

def create(name, queue_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage queue policy create", locals())


def delete(name, queue_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage queue policy delete", locals())


def show(name, queue_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage queue policy show", locals())


def list(queue_name, account_key=None, account_name=None, connection_string=None, sas_token=None):
    return call_az("az storage queue policy list", locals())


def update(name, queue_name, account_key=None, account_name=None, connection_string=None, expiry=None, permissions=None, sas_token=None, start=None):
    return call_az("az storage queue policy update", locals())

