from .... pyaz_utils import call_az

def add(account_name, name, resource_group):
    '''
    Attach a secondary storage to an Azure Media Services account.
    '''
    return call_az("az ams account storage add", locals())


def remove(account_name, name, resource_group):
    '''
    Detach a secondary storage from an Azure Media Services account.
    '''
    return call_az("az ams account storage remove", locals())


def set_authentication(account_name, resource_group, storage_auth):
    '''
    Set the authentication of a storage account attached to an Azure Media Services account.
    '''
    return call_az("az ams account storage set-authentication", locals())


def sync_storage_keys(account_name, resource_group, storage_account_id):
    '''
    Synchronize storage account keys for a storage account associated with an Azure Media Services account.
    '''
    return call_az("az ams account storage sync-storage-keys", locals())

