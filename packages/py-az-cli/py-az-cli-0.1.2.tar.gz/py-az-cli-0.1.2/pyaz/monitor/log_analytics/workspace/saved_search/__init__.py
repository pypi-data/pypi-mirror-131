from ..... pyaz_utils import call_az

def create(category, display_name, name, resource_group, saved_query, workspace_name, func_alias=None, func_param=None, tags=None):
    '''
    Create a saved search for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace saved-search create", locals())


def update(name, resource_group, workspace_name, add=None, category=None, display_name=None, force_string=None, func_alias=None, func_param=None, remove=None, saved_query=None, set=None, tags=None):
    '''
    Update a saved search for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace saved-search update", locals())


def delete(name, resource_group, workspace_name, yes=None):
    '''
    Delete a saved search for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace saved-search delete", locals())


def show(name, resource_group, workspace_name):
    '''
    Show a saved search for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace saved-search show", locals())


def list(resource_group, workspace_name):
    '''
    List all saved searches for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace saved-search list", locals())

