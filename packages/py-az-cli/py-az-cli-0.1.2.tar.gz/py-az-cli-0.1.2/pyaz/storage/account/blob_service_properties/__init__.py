from .... pyaz_utils import call_az

def show(account_name, resource_group=None):
    '''
    Show the properties of a storage account's blob service.
    '''
    return call_az("az storage account blob-service-properties show", locals())


def update(account_name, add=None, change_feed_retention_days=None, container_delete_retention_days=None, default_service_version=None, delete_retention_days=None, enable_change_feed=None, enable_container_delete_retention=None, enable_delete_retention=None, enable_last_access_tracking=None, enable_restore_policy=None, enable_versioning=None, force_string=None, remove=None, resource_group=None, restore_days=None, set=None):
    '''
    Update the properties of a storage account's blob service.
    '''
    return call_az("az storage account blob-service-properties update", locals())

