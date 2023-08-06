from ..... pyaz_utils import _call_az

def update(metadata, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return _call_az("az storage fs file metadata update", locals())


def show(account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Return all user-defined metadata for the specified file.
    '''
    return _call_az("az storage fs file metadata show", locals())

