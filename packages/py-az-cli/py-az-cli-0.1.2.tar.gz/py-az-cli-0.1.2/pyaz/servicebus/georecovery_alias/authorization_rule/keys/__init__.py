from ..... pyaz_utils import call_az

def list(alias, name, namespace_name, resource_group):
    '''
    List the keys and connection strings of Authorization Rule for the Service Bus Namespace
    '''
    return call_az("az servicebus georecovery-alias authorization-rule keys list", locals())

