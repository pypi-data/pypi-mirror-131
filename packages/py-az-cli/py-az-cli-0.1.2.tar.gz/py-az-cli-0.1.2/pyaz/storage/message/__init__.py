from ... pyaz_utils import call_az

def put(content, queue_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, time_to_live=None, timeout=None, visibility_timeout=None):
    return call_az("az storage message put", locals())


def get(queue_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, num_messages=None, sas_token=None, timeout=None, visibility_timeout=None):
    return call_az("az storage message get", locals())


def peek(queue_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, num_messages=None, sas_token=None, timeout=None):
    return call_az("az storage message peek", locals())


def delete(id, pop_receipt, queue_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage message delete", locals())


def clear(queue_name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage message clear", locals())


def update(id, pop_receipt, queue_name, visibility_timeout, account_key=None, account_name=None, auth_mode=None, connection_string=None, content=None, sas_token=None, timeout=None):
    return call_az("az storage message update", locals())

