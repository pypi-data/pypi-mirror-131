from .. pyaz_utils import call_az
from . import api, nv


def create(name, publisher_email, publisher_name, resource_group, enable_client_certificate=None, enable_managed_identity=None, location=None, no_wait=None, sku_capacity=None, sku_name=None, tags=None, virtual_network=None):
    '''
    Create an API Management service instance.
    '''
    return call_az("az apim create", locals())


def show(name, resource_group):
    '''
    Show details of an API Management service instance.
    '''
    return call_az("az apim show", locals())


def list(resource_group=None):
    '''
    List API Management service instances.
    '''
    return call_az("az apim list", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Deletes an API Management service.
    '''
    return call_az("az apim delete", locals())


def update(name, resource_group, add=None, enable_client_certificate=None, enable_managed_identity=None, force_string=None, no_wait=None, publisher_email=None, publisher_name=None, remove=None, set=None, sku_capacity=None, sku_name=None, tags=None, virtual_network=None):
    '''
    Update an API Management service instance.
    '''
    return call_az("az apim update", locals())


def check_name(name):
    return call_az("az apim check-name", locals())


def backup(backup_name, name, resource_group, storage_account_container, storage_account_key, storage_account_name, no_wait=None):
    '''
    Creates a backup of the API Management service to the given Azure Storage Account. This is long running operation and could take several minutes to complete.
    '''
    return call_az("az apim backup", locals())


def restore(backup_name, name, resource_group, storage_account_container, storage_account_key, storage_account_name, no_wait=None):
    '''
    Restores a backup of an API Management service created using the ApiManagementService_Backup operation on the current service. This is a long running operation and could take several minutes to complete.
    '''
    return call_az("az apim restore", locals())


def apply_network_updates(name, resource_group, location=None, no_wait=None):
    return call_az("az apim apply-network-updates", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of an apim is met.
    '''
    return call_az("az apim wait", locals())

