from ... pyaz_utils import call_az
from . import blob_inventory_policy, blob_service_properties, encryption_scope, file_service_properties, hns_migration, keys, management_policy, network_rule, or_policy, private_endpoint_connection, private_link_resource


def check_name(name):
    '''
    Check that the storage account name is valid and is not already in use.
    '''
    return call_az("az storage account check-name", locals())


def create(name, resource_group, access_tier=None, action=None, allow_blob_public_access=None, allow_cross_tenant_replication=None, allow_protected_append_writes=None, allow_shared_key_access=None, assign_identity=None, azure_storage_sid=None, bypass=None, custom_domain=None, default_action=None, default_share_permission=None, domain_guid=None, domain_name=None, domain_sid=None, edge_zone=None, enable_alw=None, enable_files_aadds=None, enable_files_adds=None, enable_hierarchical_namespace=None, enable_large_file_share=None, enable_nfs_v3=None, encryption_key_name=None, encryption_key_source=None, encryption_key_type_for_queue=None, encryption_key_type_for_table=None, encryption_key_vault=None, encryption_key_version=None, encryption_services=None, forest_name=None, https_only=None, identity_type=None, immutability_period_in_days=None, immutability_state=None, key_expiration_period_in_days=None, key_vault_user_identity_id=None, kind=None, location=None, min_tls_version=None, net_bios_domain_name=None, public_network_access=None, publish_internet_endpoints=None, publish_microsoft_endpoints=None, require_infrastructure_encryption=None, routing_choice=None, sas_expiration_period=None, sku=None, subnet=None, tags=None, user_identity_id=None, vnet_name=None):
    '''
    Create a storage account.
    '''
    return call_az("az storage account create", locals())


def delete(name, resource_group=None, yes=None):
    '''
    Delete a storage account.
    '''
    return call_az("az storage account delete", locals())


def show(name, expand=None, resource_group=None):
    '''
    Show storage account properties.
    '''
    return call_az("az storage account show", locals())


def list(resource_group=None):
    '''
    List storage accounts.
    '''
    return call_az("az storage account list", locals())


def show_usage(location):
    '''
    Show the current count and limit of the storage accounts under the subscription.
    '''
    return call_az("az storage account show-usage", locals())


def show_connection_string(name, blob_endpoint=None, file_endpoint=None, key=None, protocol=None, queue_endpoint=None, resource_group=None, sas_token=None, table_endpoint=None):
    '''
    Get the connection string for a storage account.
    '''
    return call_az("az storage account show-connection-string", locals())


def update(name, access_tier=None, add=None, allow_blob_public_access=None, allow_cross_tenant_replication=None, allow_protected_append_writes=None, allow_shared_key_access=None, assign_identity=None, azure_storage_sid=None, bypass=None, custom_domain=None, default_action=None, default_share_permission=None, domain_guid=None, domain_name=None, domain_sid=None, enable_files_aadds=None, enable_files_adds=None, enable_large_file_share=None, encryption_key_name=None, encryption_key_source=None, encryption_key_vault=None, encryption_key_version=None, encryption_services=None, force_string=None, forest_name=None, https_only=None, identity_type=None, immutability_period_in_days=None, immutability_state=None, key_expiration_period_in_days=None, key_vault_user_identity_id=None, min_tls_version=None, net_bios_domain_name=None, public_network_access=None, publish_internet_endpoints=None, publish_microsoft_endpoints=None, remove=None, resource_group=None, routing_choice=None, sas_expiration_period=None, set=None, sku=None, tags=None, use_subdomain=None, user_identity_id=None):
    '''
    Update the properties of a storage account.
    '''
    return call_az("az storage account update", locals())


def failover(name, no_wait=None, resource_group=None, yes=None):
    '''
    Failover request can be triggered for a storage account in case of availability issues.
    '''
    return call_az("az storage account failover", locals())


def revoke_delegation_keys(name, resource_group=None):
    '''
    Revoke all user delegation keys for a storage account.
    '''
    return call_az("az storage account revoke-delegation-keys", locals())


def generate_sas(expiry, permissions, resource_types, services, account_key=None, account_name=None, connection_string=None, https_only=None, ip=None, start=None):
    '''
    Generate a shared access signature for the storage account.
    '''
    return call_az("az storage account generate-sas", locals())

