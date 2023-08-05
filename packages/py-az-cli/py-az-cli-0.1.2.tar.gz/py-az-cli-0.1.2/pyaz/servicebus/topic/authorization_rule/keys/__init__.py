from ..... pyaz_utils import call_az

def list(name, namespace_name, resource_group, topic_name):
    '''
    List the keys and connection strings of Authorization Rule for Service Bus Topic.
    '''
    return call_az("az servicebus topic authorization-rule keys list", locals())


def renew(name, namespace_name, resource_group, topic_name, key=None, key_value=None):
    '''
    Regenerate keys of Authorization Rule for Service Bus Topic.
    '''
    return call_az("az servicebus topic authorization-rule keys renew", locals())

