from .... pyaz_utils import call_az
from . import recommendation


def list(name, resource_group, server, count=None, filter=None, skip_token=None):
    '''
    Get the sensitivity classifications of a given database.
    '''
    return call_az("az sql db classification list", locals())


def show(column, name, resource_group, schema, server, table):
    '''
    Get the sensitivity classification of a given column.
    '''
    return call_az("az sql db classification show", locals())


def delete(column, name, resource_group, schema, server, table):
    '''
    Delete the sensitivity classification of a given column.
    '''
    return call_az("az sql db classification delete", locals())


def update(column, name, resource_group, schema, server, table, information_type=None, label=None):
    '''
    Update a columns's sensitivity classification.
    '''
    return call_az("az sql db classification update", locals())

