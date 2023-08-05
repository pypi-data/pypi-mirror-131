from ... pyaz_utils import call_az

def create(name, storage_account, default_encryption_scope=None, deny_encryption_scope_override=None, enable_vlw=None, fail_on_exist=None, metadata=None, public_access=None, resource_group=None, root_squash=None):
    '''
    Create a new container under the specified storage account.
    '''
    return call_az("az storage container-rm create", locals())


def delete(name, storage_account, resource_group=None, yes=None):
    '''
    Delete the specified container under its account.
    '''
    return call_az("az storage container-rm delete", locals())


def update(name, storage_account, add=None, default_encryption_scope=None, deny_encryption_scope_override=None, force_string=None, metadata=None, public_access=None, remove=None, resource_group=None, root_squash=None, set=None):
    '''
    Update the properties for a container.
    '''
    return call_az("az storage container-rm update", locals())


def list(storage_account, include_deleted=None, resource_group=None):
    '''
    List all containers under the specified storage account.
    '''
    return call_az("az storage container-rm list", locals())


def exists(name, storage_account, resource_group=None):
    '''
    Check for the existence of a container.
    '''
    return call_az("az storage container-rm exists", locals())


def show(name, storage_account, resource_group=None):
    '''
    Show the properties for a specified container.
    '''
    return call_az("az storage container-rm show", locals())


def migrate_vlw(name, storage_account, no_wait=None, resource_group=None):
    '''
    Migrate a blob container from container level WORM to object level immutability enabled container.
    '''
    return call_az("az storage container-rm migrate-vlw", locals())

