from ..... pyaz_utils import call_az

def list(name, namespace_name, queue_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for the given Service Bus Queue
    '''
    return call_az("az servicebus queue authorization-rule keys list", locals())


def renew(name, namespace_name, queue_name, resource_group, key=None, key_value=None):
    '''
    Regenerate keys of Authorization Rule for Service Bus Queue
    '''
    return call_az("az servicebus queue authorization-rule keys renew", locals())

