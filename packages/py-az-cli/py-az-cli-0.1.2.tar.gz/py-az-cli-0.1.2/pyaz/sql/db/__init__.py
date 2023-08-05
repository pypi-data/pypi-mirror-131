from ... pyaz_utils import call_az
from . import audit_policy, classification, ledger_digest_uploads, ltr_backup, ltr_policy, op, replica, str_policy, tde, threat_policy


def show_connection_string(client, auth_type=None, name=None, server=None):
    '''
    Generates a connection string to a database.
    '''
    return call_az("az sql db show-connection-string", locals())


def create(name, resource_group, server, auto_pause_delay=None, backup_storage_redundancy=None, capacity=None, catalog_collation=None, collation=None, compute_model=None, elastic_pool=None, family=None, ledger_on=None, license_type=None, maint_config_id=None, max_size=None, min_capacity=None, no_wait=None, read_replicas=None, read_scale=None, sample_name=None, service_objective=None, tags=None, tier=None, yes=None, zone_redundant=None):
    '''
    Create a database.
    '''
    return call_az("az sql db create", locals())


def copy(dest_name, name, resource_group, server, auto_pause_delay=None, backup_storage_redundancy=None, capacity=None, compute_model=None, dest_resource_group=None, dest_server=None, elastic_pool=None, family=None, license_type=None, min_capacity=None, no_wait=None, read_replicas=None, read_scale=None, service_objective=None, tags=None, zone_redundant=None):
    '''
    Create a copy of a database.
    '''
    return call_az("az sql db copy", locals())


def restore(dest_name, name, resource_group, server, auto_pause_delay=None, backup_storage_redundancy=None, capacity=None, compute_model=None, deleted_time=None, elastic_pool=None, family=None, license_type=None, min_capacity=None, no_wait=None, read_replicas=None, read_scale=None, service_objective=None, tags=None, tier=None, time=None, zone_redundant=None):
    '''
    Create a new database by restoring from a backup.
    '''
    return call_az("az sql db restore", locals())


def rename(name, new_name, resource_group, server):
    '''
    Rename a database.
    '''
    return call_az("az sql db rename", locals())


def show(name, resource_group, server):
    '''
    Get the details for a database.
    '''
    return call_az("az sql db show", locals())


def list(resource_group, server, elastic_pool=None):
    '''
    List databases on a server or elastic pool.
    '''
    return call_az("az sql db list", locals())


def delete(name, resource_group, server, no_wait=None, yes=None):
    '''
    Delete a database.
    '''
    return call_az("az sql db delete", locals())


def update(name, resource_group, server, add=None, auto_pause_delay=None, backup_storage_redundancy=None, capacity=None, compute_model=None, elastic_pool=None, family=None, force_string=None, maint_config_id=None, max_size=None, min_capacity=None, no_wait=None, read_replicas=None, read_scale=None, remove=None, service_objective=None, set=None, tier=None, zone_redundant=None):
    '''
    Update a database.
    '''
    return call_az("az sql db update", locals())


def export(admin_password, admin_user, name, resource_group, server, storage_key, storage_key_type, storage_uri, auth_type=None):
    '''
    Export a database to a bacpac.
    '''
    return call_az("az sql db export", locals())


def import_(admin_password, admin_user, name, resource_group, server, storage_key, storage_key_type, storage_uri, auth_type=None):
    '''
    Imports a bacpac into an existing database.
    '''
    return call_az("az sql db import", locals())


def list_editions(location, available=None, dtu=None, service_objective=None, show_details=None, tier=None, vcores=None):
    '''
    Show database editions available for the currently active subscription.
    '''
    return call_az("az sql db list-editions", locals())


def list_deleted(resource_group, server):
    return call_az("az sql db list-deleted", locals())


def list_usages(name, resource_group, server):
    return call_az("az sql db list-usages", locals())

