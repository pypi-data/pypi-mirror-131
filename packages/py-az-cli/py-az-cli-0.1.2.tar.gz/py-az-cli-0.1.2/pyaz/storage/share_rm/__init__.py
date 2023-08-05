from ... pyaz_utils import call_az

def create(name, storage_account, access_tier=None, enabled_protocols=None, metadata=None, quota=None, resource_group=None, root_squash=None):
    '''
    Create a new Azure file share under the specified storage account.
    '''
    return call_az("az storage share-rm create", locals())


def delete(name, storage_account, include=None, resource_group=None, snapshot=None, yes=None):
    '''
    Delete the specified Azure file share or share snapshot.
    '''
    return call_az("az storage share-rm delete", locals())


def exists(name, storage_account, resource_group=None):
    '''
    Check for the existence of an Azure file share.
    '''
    return call_az("az storage share-rm exists", locals())


def list(storage_account, include_deleted=None, include_snapshot=None, resource_group=None):
    '''
    List the Azure file shares under the specified storage account.
    '''
    return call_az("az storage share-rm list", locals())


def show(name, storage_account, expand=None, resource_group=None, snapshot=None):
    '''
    Show the properties for a specified Azure file share or share snapshot.
    '''
    return call_az("az storage share-rm show", locals())


def update(name, storage_account, access_tier=None, add=None, force_string=None, metadata=None, quota=None, remove=None, resource_group=None, root_squash=None, set=None):
    '''
    Update the properties for an Azure file share.
    '''
    return call_az("az storage share-rm update", locals())


def stats(name, storage_account, resource_group=None):
    '''
    Get the usage bytes of the data stored on the share.
    '''
    return call_az("az storage share-rm stats", locals())


def restore(deleted_version, name, storage_account, resource_group=None, restored_name=None):
    '''
    Restore a file share within a valid retention days if share soft delete is enabled.
    '''
    return call_az("az storage share-rm restore", locals())


def snapshot(name, storage_account, access_tier=None, enabled_protocols=None, metadata=None, quota=None, resource_group=None, root_squash=None):
    '''
    Create a snapshot of an existing share under the specified account.
    '''
    return call_az("az storage share-rm snapshot", locals())

