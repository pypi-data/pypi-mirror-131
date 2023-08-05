from .... pyaz_utils import call_az

def set(managed_instance, name, resource_group, retention_days, deleted_time=None, no_wait=None):
    '''
    Update short term retention for automated backups on a single database.
    '''
    return call_az("az sql midb short-term-retention-policy set", locals())


def show(managed_instance, name, resource_group, deleted_time=None):
    '''
    Show short term retention for automated backups on a single database.
    '''
    return call_az("az sql midb short-term-retention-policy show", locals())

