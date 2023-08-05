from ... pyaz_utils import call_az

def list(id=None, include_managed=None, maxresults=None, vault_name=None):
    return call_az("az keyvault secret list", locals())


def list_versions(id=None, maxresults=None, name=None, vault_name=None):
    return call_az("az keyvault secret list-versions", locals())


def list_deleted(vault_name, id=None, maxresults=None):
    return call_az("az keyvault secret list-deleted", locals())


def set(name, vault_name, description=None, disabled=None, encoding=None, expires=None, file=None, not_before=None, secret_attributes=None, tags=None, value=None):
    '''
    Create a secret (if one doesn't exist) or update a secret in a KeyVault.
    '''
    return call_az("az keyvault secret set", locals())


def set_attributes(content_type=None, enabled=None, expires=None, id=None, name=None, not_before=None, secret_attributes=None, tags=None, vault_name=None, version=None):
    return call_az("az keyvault secret set-attributes", locals())


def show(id=None, name=None, vault_name=None, version=None):
    return call_az("az keyvault secret show", locals())


def show_deleted(id=None, name=None, vault_name=None):
    return call_az("az keyvault secret show-deleted", locals())


def delete(id=None, name=None, vault_name=None):
    return call_az("az keyvault secret delete", locals())


def purge(id=None, name=None, vault_name=None):
    return call_az("az keyvault secret purge", locals())


def recover(id=None, name=None, vault_name=None):
    return call_az("az keyvault secret recover", locals())


def download(file, encoding=None, id=None, name=None, vault_name=None, version=None):
    return call_az("az keyvault secret download", locals())


def backup(file, id=None, name=None, vault_name=None):
    return call_az("az keyvault secret backup", locals())


def restore(file, vault_name):
    return call_az("az keyvault secret restore", locals())

