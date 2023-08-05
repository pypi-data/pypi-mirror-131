from ... pyaz_utils import call_az
from . import autostorage_keys, keys


def list(resource_group=None):
    '''
    List the Batch accounts associated with a subscription or resource group.
    '''
    return call_az("az batch account list", locals())


def show(name=None, resource_group=None):
    '''
    Get a specified Batch account or the currently set account.
    '''
    return call_az("az batch account show", locals())


def create(location, name, resource_group, encryption_key_identifier=None, encryption_key_source=None, identity_type=None, keyvault=None, no_wait=None, public_network_access=None, storage_account=None, tags=None):
    '''
    Create a Batch account with the specified parameters.
    '''
    return call_az("az batch account create", locals())


def set(name, resource_group, encryption_key_identifier=None, encryption_key_source=None, identity_type=None, storage_account=None, tags=None):
    '''
    Update properties for a Batch account.
    '''
    return call_az("az batch account set", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    return call_az("az batch account delete", locals())


def login(name, resource_group, shared_key_auth=None, show=None):
    '''
    Log in to a Batch account through Azure Active Directory or Shared Key authentication.
    '''
    return call_az("az batch account login", locals())


def outbound_endpoints(name, resource_group):
    '''
    List an account's outbound network dependencies.
    '''
    return call_az("az batch account outbound-endpoints", locals())

