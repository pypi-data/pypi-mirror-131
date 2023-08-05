from ... pyaz_utils import call_az

def show(account_name, name, resource_group):
    '''
    Show the details of an asset.
    '''
    return call_az("az ams asset show", locals())


def list(account_name, resource_group, filter=None, orderby=None, top=None):
    '''
    List all the assets of an Azure Media Services account.
    '''
    return call_az("az ams asset list", locals())


def delete(account_name, name, resource_group):
    '''
    Delete an asset.
    '''
    return call_az("az ams asset delete", locals())


def list_streaming_locators(account_name, name, resource_group):
    '''
    List streaming locators which are associated with this asset.
    '''
    return call_az("az ams asset list-streaming-locators", locals())


def get_encryption_key(account_name, name, resource_group):
    '''
    Get the asset storage encryption keys used to decrypt content created by version 2 of the Media Services API.
    '''
    return call_az("az ams asset get-encryption-key", locals())


def update(account_name, name, resource_group, add=None, alternate_id=None, description=None, force_string=None, remove=None, set=None):
    '''
    Update the details of an asset.
    '''
    return call_az("az ams asset update", locals())


def get_sas_urls(account_name, name, resource_group, expiry=None, permissions=None):
    '''
    Lists storage container URLs with shared access signatures (SAS) for uploading and downloading Asset content. The signatures are derived from the storage account keys.
    '''
    return call_az("az ams asset get-sas-urls", locals())


def create(account_name, name, resource_group, alternate_id=None, container=None, description=None, storage_account=None):
    '''
    Create an asset.
    '''
    return call_az("az ams asset create", locals())

