from .... pyaz_utils import call_az

def approve(account_name, pool_name, resource_group, volume_name, remote_volume_resource_id=None):
    '''
    Authorize a volume as a replication destination for a specified source.
    '''
    return call_az("az netappfiles volume replication approve", locals())


def suspend(account_name, pool_name, resource_group, volume_name, force=None):
    '''
    Suspend/break a volume replication for the specified destination volume. The replication process is suspended until resumed or deleted.
    '''
    return call_az("az netappfiles volume replication suspend", locals())


def resume(account_name, pool_name, resource_group, volume_name):
    '''
    Resync a volume replication for the specified destination volume. The replication process is resumed from source to destination.
    '''
    return call_az("az netappfiles volume replication resume", locals())


def remove(account_name, pool_name, resource_group, volume_name):
    '''
    Delete a volume replication for the specified destination volume. The data replication objects of source and destination volumes will be removed.
    '''
    return call_az("az netappfiles volume replication remove", locals())


def status(account_name, pool_name, resource_group, volume_name):
    '''
    Get the replication status for the specified replication volume.
    '''
    return call_az("az netappfiles volume replication status", locals())


def re_initialize(account_name, pool_name, resource_group, volume_name):
    '''
    Re-initialise a volume replication for the specified destination volume. The replication process is resumed from source to destination.
    '''
    return call_az("az netappfiles volume replication re-initialize", locals())

