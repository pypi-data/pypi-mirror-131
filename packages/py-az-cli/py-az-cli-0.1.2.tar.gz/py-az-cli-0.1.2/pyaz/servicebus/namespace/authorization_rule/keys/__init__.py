from ..... pyaz_utils import call_az

def list(name, namespace_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for Service Bus Namespace
    '''
    return call_az("az servicebus namespace authorization-rule keys list", locals())


def renew(key, name, namespace_name, resource_group):
    '''
    Regenerate keys of Authorization Rule for the Service Bus Namespace.
    '''
    return call_az("az servicebus namespace authorization-rule keys renew", locals())

