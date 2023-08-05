from ... pyaz_utils import call_az
from . import authorization_rule


def set(alias, namespace_name, partner_namespace, resource_group, alternate_name=None):
    '''
    Sets a Geo-Disaster Recovery Configuration Alias for the give Namespace
    '''
    return call_az("az eventhubs georecovery-alias set", locals())


def show(alias, namespace_name, resource_group):
    '''
    shows properties of Geo-Disaster Recovery Configuration Alias for Primay or Secondary Namespace
    '''
    return call_az("az eventhubs georecovery-alias show", locals())


def list(namespace_name, resource_group):
    return call_az("az eventhubs georecovery-alias list", locals())


def break_pair(alias, namespace_name, resource_group):
    '''
    Disables Geo-Disaster Recovery Configuration Alias and stops replicating changes from primary to secondary namespaces
    '''
    return call_az("az eventhubs georecovery-alias break-pair", locals())


def fail_over(alias, namespace_name, resource_group):
    '''
    Invokes Geo-Disaster Recovery Configuration Alias to point to the secondary namespace
    '''
    return call_az("az eventhubs georecovery-alias fail-over", locals())


def exists(alias, namespace_name, resource_group):
    '''
    Check the availability of Geo-Disaster Recovery Configuration Alias Name
    '''
    return call_az("az eventhubs georecovery-alias exists", locals())


def delete(alias, namespace_name, resource_group):
    '''
    Delete Geo-Disaster Recovery Configuration Alias
    '''
    return call_az("az eventhubs georecovery-alias delete", locals())

