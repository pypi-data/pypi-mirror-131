from ... pyaz_utils import call_az
from . import sas_definition


def add(active_key_name, name, resource_id, vault_name, auto_regenerate_key=None, disabled=None, regeneration_period=None, tags=None):
    return call_az("az keyvault storage add", locals())


def list(vault_name, maxresults=None):
    return call_az("az keyvault storage list", locals())


def show(id=None, name=None, vault_name=None):
    return call_az("az keyvault storage show", locals())


def update(active_key_name=None, auto_regenerate_key=None, disabled=None, id=None, name=None, regeneration_period=None, tags=None, vault_name=None):
    return call_az("az keyvault storage update", locals())


def remove(id=None, name=None, vault_name=None):
    '''
    Remove a Key Vault managed Azure Storage Account and all associated SAS definitions. This operation requires the storage/delete permission.
    '''
    return call_az("az keyvault storage remove", locals())


def regenerate_key(key_name, id=None, name=None, vault_name=None):
    return call_az("az keyvault storage regenerate-key", locals())


def list_deleted(vault_name, maxresults=None):
    return call_az("az keyvault storage list-deleted", locals())


def show_deleted(name, vault_name):
    return call_az("az keyvault storage show-deleted", locals())


def purge(name, vault_name):
    return call_az("az keyvault storage purge", locals())


def recover(name, vault_name):
    return call_az("az keyvault storage recover", locals())


def backup(file, id=None, name=None, vault_name=None):
    return call_az("az keyvault storage backup", locals())


def restore(file, vault_name):
    return call_az("az keyvault storage restore", locals())

