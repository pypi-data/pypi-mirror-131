from ..... pyaz_utils import _call_az

def list(eventhub_name, name, namespace_name, resource_group):
    '''
    Shows the connection strings of Authorizationrule for the Eventhub.
    '''
    return _call_az("az eventhubs eventhub authorization-rule keys list", locals())


def renew(eventhub_name, key, name, namespace_name, resource_group, key_value=None):
    '''
    Regenerate the connection strings of Authorizationrule for the namespace.
    '''
    return _call_az("az eventhubs eventhub authorization-rule keys renew", locals())

