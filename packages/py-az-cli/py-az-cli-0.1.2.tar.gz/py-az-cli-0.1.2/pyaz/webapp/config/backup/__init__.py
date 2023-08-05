from .... pyaz_utils import call_az

def list(resource_group, webapp_name, slot=None):
    '''
    List backups of a web app.
    '''
    return call_az("az webapp config backup list", locals())


def show(resource_group, webapp_name, slot=None):
    '''
    Show the backup schedule for a web app.
    '''
    return call_az("az webapp config backup show", locals())


def create(container_url, resource_group, webapp_name, backup_name=None, db_connection_string=None, db_name=None, db_type=None, slot=None):
    '''
    Create a backup of a web app.
    '''
    return call_az("az webapp config backup create", locals())


def update(resource_group, webapp_name, backup_name=None, container_url=None, db_connection_string=None, db_name=None, db_type=None, frequency=None, retain_one=None, retention=None, slot=None):
    '''
    Configure a new backup schedule for a web app.
    '''
    return call_az("az webapp config backup update", locals())


def restore(backup_name, container_url, resource_group, webapp_name, db_connection_string=None, db_name=None, db_type=None, ignore_hostname_conflict=None, overwrite=None, slot=None, target_name=None):
    '''
    Restore a web app from a backup.
    '''
    return call_az("az webapp config backup restore", locals())

