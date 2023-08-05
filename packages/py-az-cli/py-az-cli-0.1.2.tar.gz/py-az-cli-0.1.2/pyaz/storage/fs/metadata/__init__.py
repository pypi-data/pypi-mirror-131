from .... pyaz_utils import call_az

def update(metadata, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    return call_az("az storage fs metadata update", locals())


def show(name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Return all user-defined metadata for the specified file system.
    '''
    return call_az("az storage fs metadata show", locals())

