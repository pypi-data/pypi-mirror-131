from .... pyaz_utils import call_az

def add(account_name, name, resource_group, base64_key=None, expiration=None, identifier=None):
    '''
    Add an AkamaiAccessControl to an existing streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint akamai add", locals())


def remove(account_name, identifier, name, resource_group):
    '''
    Remove an AkamaiAccessControl from an existing streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint akamai remove", locals())

