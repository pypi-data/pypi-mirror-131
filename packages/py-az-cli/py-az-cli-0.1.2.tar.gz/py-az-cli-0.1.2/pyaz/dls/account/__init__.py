from ... pyaz_utils import call_az
from . import firewall, network_rule, trusted_provider


def create(account, default_group=None, disable_encryption=None, encryption_type=None, key_name=None, key_vault_id=None, key_version=None, location=None, resource_group=None, tags=None, tier=None):
    '''
    Creates a Data Lake Store account.
    '''
    return call_az("az dls account create", locals())


def update(account, allow_azure_ips=None, default_group=None, firewall_state=None, key_version=None, resource_group=None, tags=None, tier=None, trusted_id_provider_state=None):
    '''
    Updates a Data Lake Store account.
    '''
    return call_az("az dls account update", locals())


def list(resource_group=None):
    '''
    Lists available Data Lake Store accounts.
    '''
    return call_az("az dls account list", locals())


def delete(account, resource_group=None):
    '''
    Delete a Data Lake Store account.
    '''
    return call_az("az dls account delete", locals())


def show(account, resource_group=None):
    '''
    Get the details of a Data Lake Store account.
    '''
    return call_az("az dls account show", locals())


def enable_key_vault(account, resource_group=None):
    '''
    Enable the use of Azure Key Vault for encryption of a Data Lake Store account.
    '''
    return call_az("az dls account enable-key-vault", locals())

