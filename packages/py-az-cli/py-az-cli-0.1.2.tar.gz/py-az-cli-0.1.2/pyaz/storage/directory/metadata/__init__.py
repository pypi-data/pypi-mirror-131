from .... pyaz_utils import call_az

def show(name, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage directory metadata show", locals())


def update(name, share_name, account_key=None, account_name=None, connection_string=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage directory metadata update", locals())

