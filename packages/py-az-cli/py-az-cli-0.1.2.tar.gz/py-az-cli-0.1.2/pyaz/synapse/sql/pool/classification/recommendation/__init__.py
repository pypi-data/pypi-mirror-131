from ...... pyaz_utils import call_az

def list(name, resource_group, workspace_name, filter=None, included_disabled=None, skip_token=None):
    '''
    List the recommended sensitivity classifications of a given SQL pool.
    '''
    return call_az("az synapse sql pool classification recommendation list", locals())


def enable(column, name, resource_group, schema, table, workspace_name):
    '''
    Enable sensitivity recommendations for a given column(recommendations are enabled by default on all columns).
    '''
    return call_az("az synapse sql pool classification recommendation enable", locals())


def disable(column, name, resource_group, schema, table, workspace_name):
    '''
    Disable sensitivity recommendations for a given column(recommendations are enabled by default on all columns).
    '''
    return call_az("az synapse sql pool classification recommendation disable", locals())

