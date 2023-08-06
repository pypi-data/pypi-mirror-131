from ..... pyaz_utils import _call_az

def list(resource_group, workspace_name):
    '''
    List all the tables for the given Log Analytics workspace.
    '''
    return _call_az("az monitor log-analytics workspace table list", locals())


def show(name, resource_group, workspace_name):
    '''
    Get a Log Analytics workspace table.
    '''
    return _call_az("az monitor log-analytics workspace table show", locals())


def update(name, resource_group, retention_time, workspace_name):
    '''
    Update the properties of a Log Analytics workspace table, currently only support updating retention time.
    '''
    return _call_az("az monitor log-analytics workspace table update", locals())

