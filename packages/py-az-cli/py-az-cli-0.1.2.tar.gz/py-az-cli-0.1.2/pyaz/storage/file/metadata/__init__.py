from .... pyaz_utils import call_az

def show(path, share_name, account_key=None, account_name=None, connection_string=None, sas_token=None, snapshot=None, timeout=None):
    return call_az("az storage file metadata show", locals())


def update(path, share_name, account_key=None, account_name=None, connection_string=None, metadata=None, sas_token=None, timeout=None):
    return call_az("az storage file metadata update", locals())

