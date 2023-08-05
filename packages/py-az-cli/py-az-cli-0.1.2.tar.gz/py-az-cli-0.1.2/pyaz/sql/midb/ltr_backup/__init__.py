from .... pyaz_utils import call_az

def show(backup_id=None, database=None, location=None, managed_instance=None, name=None):
    '''
    Get a long term retention backup for a managed database.
    '''
    return call_az("az sql midb ltr-backup show", locals())


def list(location, database=None, database_state=None, managed_instance=None, only_latest_per_database=None, resource_group=None):
    '''
    List the long term retention backups for a location, instance or database.
    '''
    return call_az("az sql midb ltr-backup list", locals())


def delete(backup_id=None, database=None, location=None, managed_instance=None, name=None, yes=None):
    '''
    Delete a long term retention backup.
    '''
    return call_az("az sql midb ltr-backup delete", locals())


def restore(backup_id, dest_database, dest_mi, dest_resource_group, no_wait=None):
    '''
    Restore a long term retention backup to a new database.
    '''
    return call_az("az sql midb ltr-backup restore", locals())


def wait(database, managed_instance, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the managed database is met.
    '''
    return call_az("az sql midb ltr-backup wait", locals())

