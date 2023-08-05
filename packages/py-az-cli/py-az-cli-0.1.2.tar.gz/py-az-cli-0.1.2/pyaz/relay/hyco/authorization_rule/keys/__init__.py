from ..... pyaz_utils import call_az

def list(hybrid_connection_name, name, namespace_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for Relay Service Hybrid Connection.
    '''
    return call_az("az relay hyco authorization-rule keys list", locals())


def renew(hybrid_connection_name, key, name, namespace_name, resource_group, key_value=None):
    '''
    Regenerate keys of Authorization Rule for Relay Service Hybrid Connection.
    '''
    return call_az("az relay hyco authorization-rule keys renew", locals())

