from ..... pyaz_utils import call_az

def create(resource_group, storage_accounts, type, workspace_name):
    '''
    Create some linked storage accounts for log analytics workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-storage create", locals())


def add(resource_group, storage_accounts, type, workspace_name):
    '''
    Add some linked storage accounts with specific data source type for log analytics workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-storage add", locals())


def remove(resource_group, storage_accounts, type, workspace_name):
    '''
    Remove some linked storage accounts with specific data source type for log analytics workspace
    '''
    return call_az("az monitor log-analytics workspace linked-storage remove", locals())


def delete(resource_group, type, workspace_name, yes=None):
    '''
    Delete all linked storage accounts with specific data source type for log analytics workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-storage delete", locals())


def show(resource_group, type, workspace_name):
    '''
    List all linked storage accounts with specific data source type for a log analytics workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-storage show", locals())


def list(resource_group, workspace_name):
    '''
    List all linked storage accounts for a log analytics workspace.
    '''
    return call_az("az monitor log-analytics workspace linked-storage list", locals())

