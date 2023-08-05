from .... pyaz_utils import call_az

def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage queue metadata show", locals())


def update(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage queue metadata update", locals())

