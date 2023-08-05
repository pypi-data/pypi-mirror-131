from ... pyaz_utils import call_az
from . import rotation_policy


def list(hsm_name=None, id=None, include_managed=None, maxresults=None, vault_name=None):
    '''
    List keys in the specified Vault or HSM.
    '''
    return call_az("az keyvault key list", locals())


def list_versions(hsm_name=None, id=None, maxresults=None, name=None, vault_name=None):
    return call_az("az keyvault key list-versions", locals())


def list_deleted(hsm_name=None, id=None, maxresults=None, vault_name=None):
    '''
    List the deleted keys in the specified Vault or HSM.
    '''
    return call_az("az keyvault key list-deleted", locals())


def show_deleted(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Get the public part of a deleted key.
    '''
    return call_az("az keyvault key show-deleted", locals())


def delete(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Delete a key of any type from storage in Vault or HSM.
    '''
    return call_az("az keyvault key delete", locals())


def purge(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Permanently delete the specified key.
    '''
    return call_az("az keyvault key purge", locals())


def recover(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Recover the deleted key to its latest version.
    '''
    return call_az("az keyvault key recover", locals())


def backup(file, hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Request that a backup of the specified key be downloaded to the client.
    '''
    return call_az("az keyvault key backup", locals())


def restore(backup_folder=None, blob_container_name=None, file=None, hsm_name=None, id=None, name=None, no_wait=None, storage_account_name=None, storage_container_SAS_token=None, storage_resource_uri=None, vault_name=None):
    '''
    Restore a backed up key to a Vault or HSM.
    '''
    return call_az("az keyvault key restore", locals())


def download(file, encoding=None, hsm_name=None, id=None, name=None, vault_name=None, version=None):
    '''
    Download the public part of a stored key.
    '''
    return call_az("az keyvault key download", locals())


def create(curve=None, disabled=None, expires=None, exportable=None, hsm_name=None, id=None, kty=None, name=None, not_before=None, ops=None, policy=None, protection=None, size=None, tags=None, vault_name=None):
    '''
    Create a new key, stores it, then returns key parameters and attributes to the client.
    '''
    return call_az("az keyvault key create", locals())


def set_attributes(enabled=None, expires=None, hsm_name=None, id=None, name=None, not_before=None, ops=None, policy=None, tags=None, vault_name=None, version=None):
    '''
    The update key operation changes specified attributes of a stored key and can be applied to any key type and key version stored in Vault or HSM.
    '''
    return call_az("az keyvault key set-attributes", locals())


def show(hsm_name=None, id=None, name=None, vault_name=None, version=None):
    return call_az("az keyvault key show", locals())


def import_(byok_file=None, byok_string=None, curve=None, disabled=None, expires=None, exportable=None, hsm_name=None, id=None, kty=None, name=None, not_before=None, ops=None, pem_file=None, pem_password=None, pem_string=None, policy=None, protection=None, tags=None, vault_name=None):
    return call_az("az keyvault key import", locals())


def get_policy_template():
    '''
    Return policy template as JSON encoded policy definition.
    '''
    return call_az("az keyvault key get-policy-template", locals())


def encrypt(algorithm, value, aad=None, data_type=None, hsm_name=None, id=None, iv=None, name=None, vault_name=None, version=None):
    '''
    Encrypt an arbitrary sequence of bytes using an encryption key that is stored in a Vault or HSM.
    '''
    return call_az("az keyvault key encrypt", locals())


def decrypt(algorithm, value, aad=None, data_type=None, hsm_name=None, id=None, iv=None, name=None, tag=None, vault_name=None, version=None):
    '''
    Decrypt a single block of encrypted data.
    '''
    return call_az("az keyvault key decrypt", locals())


def random(count, hsm_name=None, id=None):
    return call_az("az keyvault key random", locals())


def rotate(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Rotate the key based on the key policy by generating a new version of the key.
    '''
    return call_az("az keyvault key rotate", locals())

