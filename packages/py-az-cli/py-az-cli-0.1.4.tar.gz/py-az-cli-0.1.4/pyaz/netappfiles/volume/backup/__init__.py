from .... pyaz_utils import _call_az

def show(account_name, backup_name, pool_name, resource_group, volume_name):
    '''
    Get the specified ANF Backup.
    '''
    return _call_az("az netappfiles volume backup show", locals())


def list(account_name, pool_name, resource_group, volume_name):
    '''
    List the ANF Backups for the specified volume.
    '''
    return _call_az("az netappfiles volume backup list", locals())


def delete(account_name, backup_name, pool_name, resource_group, volume_name):
    return _call_az("az netappfiles volume backup delete", locals())


def status(account_name, pool_name, resource_group, volume_name):
    '''
    Get backup status of the specified ANF Volume.
    '''
    return _call_az("az netappfiles volume backup status", locals())


def restore_status(account_name, pool_name, resource_group, volume_name):
    '''
    Get backup restore status of the specified ANF Volume.
    '''
    return _call_az("az netappfiles volume backup restore-status", locals())


def update(account_name, backup_name, pool_name, resource_group, volume_name, label=None, tags=None, use_existing_snapshot=None):
    '''
    Update the specified ANF backup with the values provided.
    '''
    return _call_az("az netappfiles volume backup update", locals())


def create(account_name, backup_name, location, pool_name, resource_group, volume_name, use_existing_snapshot=None):
    '''
    Create specified ANF volume backup.
    '''
    return _call_az("az netappfiles volume backup create", locals())

