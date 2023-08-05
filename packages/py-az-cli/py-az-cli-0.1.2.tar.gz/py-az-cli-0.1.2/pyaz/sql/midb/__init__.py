from ... pyaz_utils import call_az
from . import log_replay, ltr_backup, ltr_policy, short_term_retention_policy


def list_deleted(managed_instance, resource_group):
    '''
    List restorable deleted managed databases.
    '''
    return call_az("az sql midb list-deleted", locals())


def create(managed_instance, name, resource_group, collation=None, no_wait=None):
    '''
    Create a managed database.
    '''
    return call_az("az sql midb create", locals())


def restore(dest_name, managed_instance, name, resource_group, time, deleted_time=None, dest_mi=None, dest_resource_group=None, no_wait=None):
    '''
    Restore a managed database.
    '''
    return call_az("az sql midb restore", locals())


def show(managed_instance, name, resource_group):
    '''
    Get the details for a managed database.
    '''
    return call_az("az sql midb show", locals())


def list(managed_instance, resource_group):
    '''
    List managed databases on a managed instance.
    '''
    return call_az("az sql midb list", locals())


def delete(managed_instance, name, resource_group, no_wait=None, yes=None):
    '''
    Delete a managed database.
    '''
    return call_az("az sql midb delete", locals())

