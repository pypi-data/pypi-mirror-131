from .... pyaz_utils import call_az

def renew(key, name, resource_group):
    '''
    Regenerate either the primary or secondary key for use with the Maps APIs. The old key will stop working immediately.
    '''
    return call_az("az maps account keys renew", locals())


def list(name, resource_group):
    '''
    Get the keys to use with the Maps APIs. A key is used to authenticate and authorize access to the Maps REST APIs. Only one key is needed at a time; two are given to provide seamless key regeneration.
    '''
    return call_az("az maps account keys list", locals())

