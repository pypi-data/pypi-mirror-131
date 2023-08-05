from .... pyaz_utils import call_az

def start(managed_instance, name, resource_group, storage_sas, storage_uri, auto_complete=None, last_backup_name=None, no_wait=None):
    '''
    Start Log Replay service on specified database.
    '''
    return call_az("az sql midb log-replay start", locals())


def stop(managed_instance, name, resource_group, no_wait=None, yes=None):
    '''
    Stop Log Replay service.
    '''
    return call_az("az sql midb log-replay stop", locals())


def complete(managed_instance, name, resource_group, last_backup_name=None):
    '''
    Complete Log Replay service on specified database.
    '''
    return call_az("az sql midb log-replay complete", locals())


def wait(managed_instance, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the managed database is met.
    '''
    return call_az("az sql midb log-replay wait", locals())


def show(managed_instance, name, resource_group):
    '''
    Get status of Log Replay service.
    '''
    return call_az("az sql midb log-replay show", locals())

