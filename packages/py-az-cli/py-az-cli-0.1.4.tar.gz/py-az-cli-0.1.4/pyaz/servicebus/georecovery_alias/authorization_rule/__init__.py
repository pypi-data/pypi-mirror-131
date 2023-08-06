from .... pyaz_utils import _call_az
from . import keys


def list(alias, namespace_name, resource_group):
    '''
    Shows the list of Authorization Rule by Service Bus Namespace
    '''
    return _call_az("az servicebus georecovery-alias authorization-rule list", locals())


def show(alias, name, namespace_name, resource_group):
    return _call_az("az servicebus georecovery-alias authorization-rule show", locals())

