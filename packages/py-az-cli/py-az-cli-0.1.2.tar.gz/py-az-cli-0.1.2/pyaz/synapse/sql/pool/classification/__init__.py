from ..... pyaz_utils import call_az
from . import recommendation


def show(column, name, resource_group, schema, table, workspace_name):
    '''
    Get the sensitivity classification of a given column.
    '''
    return call_az("az synapse sql pool classification show", locals())


def list(name, resource_group, workspace_name, filter=None):
    '''
    Get the sensitivity classifications of a given SQL pool.
    '''
    return call_az("az synapse sql pool classification list", locals())


def create(column, information_type, label, name, resource_group, schema, table, workspace_name):
    '''
    Create a column's sensitivity classification.
    '''
    return call_az("az synapse sql pool classification create", locals())


def delete(column, name, resource_group, schema, table, workspace_name):
    '''
    Delete the sensitivity classification of a given column.
    '''
    return call_az("az synapse sql pool classification delete", locals())


def update(column, name, resource_group, schema, table, workspace_name, information_type=None, label=None):
    '''
    Update a column's sensitivity classification.
    '''
    return call_az("az synapse sql pool classification update", locals())

