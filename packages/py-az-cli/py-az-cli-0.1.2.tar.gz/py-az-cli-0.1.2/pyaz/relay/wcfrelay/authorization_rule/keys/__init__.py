from ..... pyaz_utils import call_az

def list(name, namespace_name, relay_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for the given Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay authorization-rule keys list", locals())


def renew(key, name, namespace_name, relay_name, resource_group, key_value=None):
    '''
    Regenerate keys of Authorization Rule for Relay Service WCF Relay
    '''
    return call_az("az relay wcfrelay authorization-rule keys renew", locals())

