from .. pyaz_utils import call_az
from . import backup, certificate, key, network_rule, private_endpoint_connection, private_link_resource, restore, secret, security_domain, storage


def create(resource_group, administrators=None, bypass=None, default_action=None, enable_purge_protection=None, enable_rbac_authorization=None, enable_soft_delete=None, enabled_for_deployment=None, enabled_for_disk_encryption=None, enabled_for_template_deployment=None, hsm_name=None, location=None, name=None, network_acls=None, network_acls_ips=None, network_acls_vnets=None, no_self_perms=None, no_wait=None, public_network_access=None, retention_days=None, sku=None, tags=None):
    '''
    Create a Vault or HSM.
    '''
    return call_az("az keyvault create", locals())


def recover(hsm_name=None, location=None, name=None, no_wait=None, resource_group=None):
    '''
    Recover a Vault or HSM.
    '''
    return call_az("az keyvault recover", locals())


def list(resource_group=None, resource_type=None):
    '''
    List Vaults and/or HSMs.
    '''
    return call_az("az keyvault list", locals())


def show(hsm_name=None, name=None, resource_group=None):
    '''
    Show details of a Vault or HSM.
    '''
    return call_az("az keyvault show", locals())


def delete(hsm_name=None, name=None, no_wait=None, resource_group=None):
    '''
    Delete a Vault or HSM.
    '''
    return call_az("az keyvault delete", locals())


def purge(hsm_name=None, location=None, name=None, no_wait=None):
    '''
    Permanently delete the specified Vault or HSM. Aka Purges the deleted Vault or HSM.
    '''
    return call_az("az keyvault purge", locals())


def set_policy(name, application_id=None, certificate_permissions=None, key_permissions=None, no_wait=None, object_id=None, resource_group=None, secret_permissions=None, spn=None, storage_permissions=None, upn=None):
    '''
    Update security policy settings for a Key Vault.
    '''
    return call_az("az keyvault set-policy", locals())


def delete_policy(name, application_id=None, no_wait=None, object_id=None, resource_group=None, spn=None, upn=None):
    return call_az("az keyvault delete-policy", locals())


def list_deleted(resource_type=None):
    '''
    Get information about the deleted Vaults or HSMs in a subscription.
    '''
    return call_az("az keyvault list-deleted", locals())


def show_deleted(hsm_name=None, location=None, name=None):
    '''
    Show details of a deleted Vault or HSM.
    '''
    return call_az("az keyvault show-deleted", locals())


def update(name, add=None, bypass=None, default_action=None, enable_purge_protection=None, enable_rbac_authorization=None, enable_soft_delete=None, enabled_for_deployment=None, enabled_for_disk_encryption=None, enabled_for_template_deployment=None, force_string=None, no_wait=None, public_network_access=None, remove=None, resource_group=None, retention_days=None, set=None):
    '''
    Update the properties of a Vault.
    '''
    return call_az("az keyvault update", locals())


def wait(name, created=None, custom=None, deleted=None, exists=None, interval=None, resource_group=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the Vault is met.
    '''
    return call_az("az keyvault wait", locals())


def update_hsm(hsm_name, add=None, bypass=None, default_action=None, enable_purge_protection=None, force_string=None, no_wait=None, remove=None, resource_group=None, secondary_locations=None, set=None):
    '''
    Update the properties of a HSM.
    '''
    return call_az("az keyvault update-hsm", locals())


def wait_hsm(hsm_name, created=None, custom=None, deleted=None, exists=None, interval=None, resource_group=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the HSM is met.
    '''
    return call_az("az keyvault wait-hsm", locals())

