from ... pyaz_utils import call_az
from . import contact, issuer, pending


def create(name, policy, vault_name, disabled=None, tags=None, validity=None):
    '''
    Create a Key Vault certificate.
    '''
    return call_az("az keyvault certificate create", locals())


def list(id=None, include_pending=None, maxresults=None, vault_name=None):
    return call_az("az keyvault certificate list", locals())


def list_versions(id=None, maxresults=None, name=None, vault_name=None):
    return call_az("az keyvault certificate list-versions", locals())


def list_deleted(vault_name, id=None, include_pending=None, maxresults=None):
    return call_az("az keyvault certificate list-deleted", locals())


def show(id=None, name=None, vault_name=None, version=None):
    return call_az("az keyvault certificate show", locals())


def show_deleted(id=None, name=None, vault_name=None):
    return call_az("az keyvault certificate show-deleted", locals())


def delete(id=None, name=None, vault_name=None):
    return call_az("az keyvault certificate delete", locals())


def purge(id=None, name=None, vault_name=None):
    return call_az("az keyvault certificate purge", locals())


def recover(id=None, name=None, vault_name=None):
    return call_az("az keyvault certificate recover", locals())


def set_attributes(certificate_attributes=None, enabled=None, id=None, name=None, policy=None, tags=None, vault_name=None, version=None):
    return call_az("az keyvault certificate set-attributes", locals())


def import_(file, name, vault_name, disabled=None, password=None, policy=None, tags=None):
    '''
    Import a certificate into KeyVault.
    '''
    return call_az("az keyvault certificate import", locals())


def download(file, encoding=None, id=None, name=None, vault_name=None, version=None):
    '''
    Download the public portion of a Key Vault certificate.
    '''
    return call_az("az keyvault certificate download", locals())


def get_default_policy(scaffold=None):
    '''
    Get the default policy for self-signed certificates.
    '''
    return call_az("az keyvault certificate get-default-policy", locals())


def backup(file, id=None, name=None, vault_name=None):
    return call_az("az keyvault certificate backup", locals())


def restore(file, vault_name):
    return call_az("az keyvault certificate restore", locals())

