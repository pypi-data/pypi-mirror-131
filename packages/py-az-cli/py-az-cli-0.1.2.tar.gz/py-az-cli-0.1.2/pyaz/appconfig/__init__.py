from .. pyaz_utils import call_az
from . import credential, feature, identity, kv, revision


def create(location, name, resource_group, assign_identity=None, disable_local_auth=None, enable_public_network=None, sku=None, tags=None):
    '''
    Create an App Configuration.
    '''
    return call_az("az appconfig create", locals())


def delete(name, resource_group=None, yes=None):
    '''
    Delete an App Configuration.
    '''
    return call_az("az appconfig delete", locals())


def update(name, disable_local_auth=None, enable_public_network=None, encryption_key_name=None, encryption_key_vault=None, encryption_key_version=None, identity_client_id=None, resource_group=None, sku=None, tags=None):
    '''
    Update an App Configuration.
    '''
    return call_az("az appconfig update", locals())


def list(resource_group=None):
    '''
    Lists all App Configurations under the current subscription.
    '''
    return call_az("az appconfig list", locals())


def show(name, resource_group=None):
    '''
    Show properties of an App Configuration.
    '''
    return call_az("az appconfig show", locals())

