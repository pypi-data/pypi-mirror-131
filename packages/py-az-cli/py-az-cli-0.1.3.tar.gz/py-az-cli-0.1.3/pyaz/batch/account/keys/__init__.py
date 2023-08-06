from .... pyaz_utils import _call_az

def list(name, resource_group):
    return _call_az("az batch account keys list", locals())


def renew(key_name=None, name=None, resource_group=None):
    '''
    Renew keys for a Batch account.
    '''
    return _call_az("az batch account keys renew", locals())

