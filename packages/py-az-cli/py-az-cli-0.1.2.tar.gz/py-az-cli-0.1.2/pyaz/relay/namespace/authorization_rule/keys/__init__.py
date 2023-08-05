from ..... pyaz_utils import call_az

def list(name, namespace_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for Relay Service Namespace
    '''
    return call_az("az relay namespace authorization-rule keys list", locals())


def renew(key, name, namespace_name, resource_group, key_value=None):
    '''
    Regenerate keys of Authorization Rule for the Relay Service Namespace.
    '''
    return call_az("az relay namespace authorization-rule keys renew", locals())

