from .... pyaz_utils import call_az

def set(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, expiry_time=None, policy_mode=None, sas_token=None, timeout=None):
    '''
    Set blob's immutability policy.
    '''
    return call_az("az storage blob immutability-policy set", locals())


def delete(container_name, name, account_key=None, account_name=None, auth_mode=None, connection_string=None, sas_token=None, timeout=None):
    '''
    Delete blob's immutability policy.
    '''
    return call_az("az storage blob immutability-policy delete", locals())

