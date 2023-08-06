from ..... pyaz_utils import _call_az

def list(name, resource_group, server, filter=None, include_disabled_recommendations=None):
    '''
    List the recommended sensitivity classifications of a given database.
    '''
    return _call_az("az sql db classification recommendation list", locals())


def enable(column, name, resource_group, schema, server, table):
    '''
    Enable sensitivity recommendations for a given column (recommendations are enabled by default on all columns).
    '''
    return _call_az("az sql db classification recommendation enable", locals())


def disable(column, name, resource_group, schema, server, table):
    '''
    Disable sensitivity recommendations for a given column (recommendations are enabled by default on all columns).
    '''
    return _call_az("az sql db classification recommendation disable", locals())

