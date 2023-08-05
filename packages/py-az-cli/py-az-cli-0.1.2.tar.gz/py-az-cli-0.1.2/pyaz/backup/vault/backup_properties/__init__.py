from .... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Gets backup related properties of the Recovery Services vault.
    '''
    return call_az("az backup vault backup-properties show", locals())


def set(name, resource_group, backup_storage_redundancy=None, cross_region_restore_flag=None, soft_delete_feature_state=None):
    '''
    Sets backup related properties of the Recovery Services vault.
    '''
    return call_az("az backup vault backup-properties set", locals())

