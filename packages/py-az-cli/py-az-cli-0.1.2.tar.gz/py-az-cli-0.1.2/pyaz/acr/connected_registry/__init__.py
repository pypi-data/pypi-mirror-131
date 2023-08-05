from ... pyaz_utils import call_az
from . import install, permissions


def create(name, registry, audit_logs_enabled=None, client_tokens=None, log_level=None, mode=None, parent=None, repository=None, resource_group=None, sync_message_ttl=None, sync_schedule=None, sync_token=None, sync_window=None):
    '''
    Create a connected registry for an Azure Container Registry.
    '''
    return call_az("az acr connected-registry create", locals())


def delete(name, registry, cleanup=None, resource_group=None, yes=None):
    '''
    Delete a connected registry from Azure Container Registry.
    '''
    return call_az("az acr connected-registry delete", locals())


def show(name, registry, resource_group=None):
    '''
    Show connected registry details.
    '''
    return call_az("az acr connected-registry show", locals())


def deactivate(name, registry, resource_group=None, yes=None):
    '''
    Deactivate a connected registry from Azure Container Registry.
    '''
    return call_az("az acr connected-registry deactivate", locals())


def update(name, registry, add_client_tokens=None, audit_logs_enabled=None, log_level=None, remove_client_tokens=None, resource_group=None, sync_message_ttl=None, sync_schedule=None, sync_window=None):
    '''
    Update a connected registry for an Azure Container Registry.
    '''
    return call_az("az acr connected-registry update", locals())


def get_settings(name, parent_protocol, registry, generate_password=None, resource_group=None, yes=None):
    '''
    Retrieve information required to activate a connected registry, and creates or rotates the sync token credentials.
    '''
    return call_az("az acr connected-registry get-settings", locals())


def list(registry, no_children=None, parent=None, resource_group=None):
    '''
    List all the connected registries under the current parent registry.
    '''
    return call_az("az acr connected-registry list", locals())


def list_client_tokens(name, registry, resource_group=None):
    '''
    List all the client tokens associated to a specific connected registries.
    '''
    return call_az("az acr connected-registry list-client-tokens", locals())


def repo(name, registry, add=None, remove=None, resource_group=None):
    '''
    Update all the necessary connected registry sync scope maps repository permissions.
    '''
    return call_az("az acr connected-registry repo", locals())

