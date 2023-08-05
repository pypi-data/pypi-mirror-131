from .... pyaz_utils import call_az
from . import data_export, linked_service, linked_storage, pack, saved_search, table


def create(resource_group, workspace_name, capacity_reservation_level=None, ingestion_access=None, location=None, no_wait=None, query_access=None, quota=None, retention_time=None, sku=None, tags=None):
    '''
    Create a workspace instance
    '''
    return call_az("az monitor log-analytics workspace create", locals())


def update(resource_group, workspace_name, add=None, capacity_reservation_level=None, force_string=None, ingestion_access=None, query_access=None, quota=None, remove=None, retention_time=None, set=None, tags=None):
    '''
    Update a workspace instance
    '''
    return call_az("az monitor log-analytics workspace update", locals())


def show(resource_group, workspace_name):
    '''
    Show a workspace instance.
    '''
    return call_az("az monitor log-analytics workspace show", locals())


def delete(resource_group, workspace_name, force=None, yes=None):
    '''
    Delete a workspace instance.
    '''
    return call_az("az monitor log-analytics workspace delete", locals())


def list(resource_group=None):
    '''
    Get a list of workspaces under a resource group or a subscription.
    '''
    return call_az("az monitor log-analytics workspace list", locals())


def list_deleted_workspaces(resource_group=None):
    '''
    Get a list of deleted workspaces that can be recovered in a subscription or a resource group.
    '''
    return call_az("az monitor log-analytics workspace list-deleted-workspaces", locals())


def recover(workspace_name, no_wait=None, resource_group=None):
    '''
    Recover a workspace in a soft-delete state within 14 days.
    '''
    return call_az("az monitor log-analytics workspace recover", locals())


def get_schema(resource_group, workspace_name):
    '''
    Get the schema for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace get-schema", locals())


def list_usages(resource_group, workspace_name):
    '''
    Get a list of usage metrics for a workspace.
    '''
    return call_az("az monitor log-analytics workspace list-usages", locals())


def list_management_groups(resource_group, workspace_name):
    '''
    Get a list of management groups connected to a workspace.
    '''
    return call_az("az monitor log-analytics workspace list-management-groups", locals())


def get_shared_keys(resource_group, workspace_name):
    '''
    Get the shared keys for a workspace.
    '''
    return call_az("az monitor log-analytics workspace get-shared-keys", locals())

