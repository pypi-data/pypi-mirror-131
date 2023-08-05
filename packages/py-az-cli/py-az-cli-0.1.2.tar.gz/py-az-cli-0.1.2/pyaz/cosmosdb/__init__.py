from .. pyaz_utils import call_az
from . import collection, database, identity, keys, locations, network_rule, private_endpoint_connection, private_link_resource, restorable_database_account, table


def show(name, resource_group):
    '''
    Get the details of an Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb show", locals())


def list_keys(name, resource_group):
    '''
    List the access keys for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb list-keys", locals())


def list_read_only_keys(name, resource_group):
    '''
    List the read-only access keys for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb list-read-only-keys", locals())


def list_connection_strings(name, resource_group):
    '''
    List the connection strings for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb list-connection-strings", locals())


def regenerate_key(key_kind, name, resource_group):
    '''
    Regenerate an access key for a Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb regenerate-key", locals())


def check_name_exists(name):
    '''
    Checks if an Azure Cosmos DB account name exists.
    '''
    return call_az("az cosmosdb check-name-exists", locals())


def delete(name, resource_group, yes=None):
    '''
    Deletes an Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb delete", locals())


def failover_priority_change(failover_policies, name, resource_group):
    '''
    Changes the failover priority for the Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb failover-priority-change", locals())


def create(name, resource_group, analytical_storage_schema_type=None, assign_identity=None, backup_interval=None, backup_policy_type=None, backup_redundancy=None, backup_retention=None, capabilities=None, databases_to_restore=None, default_consistency_level=None, default_identity=None, disable_key_based_metadata_write_access=None, enable_analytical_storage=None, enable_automatic_failover=None, enable_free_tier=None, enable_multiple_write_locations=None, enable_public_network=None, enable_virtual_network=None, ip_range_filter=None, is_restore_request=None, key_uri=None, kind=None, locations=None, max_interval=None, max_staleness_prefix=None, network_acl_bypass=None, network_acl_bypass_resource_ids=None, restore_source=None, restore_timestamp=None, server_version=None, tags=None, virtual_network_rules=None):
    '''
    Creates a new Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb create", locals())


def update(name, resource_group, analytical_storage_schema_type=None, backup_interval=None, backup_policy_type=None, backup_redundancy=None, backup_retention=None, capabilities=None, default_consistency_level=None, default_identity=None, disable_key_based_metadata_write_access=None, enable_analytical_storage=None, enable_automatic_failover=None, enable_multiple_write_locations=None, enable_public_network=None, enable_virtual_network=None, ip_range_filter=None, locations=None, max_interval=None, max_staleness_prefix=None, network_acl_bypass=None, network_acl_bypass_resource_ids=None, server_version=None, tags=None, virtual_network_rules=None):
    '''
    Update an Azure Cosmos DB database account.
    '''
    return call_az("az cosmosdb update", locals())


def list(resource_group=None):
    '''
    List Azure Cosmos DB database accounts.
    '''
    return call_az("az cosmosdb list", locals())


def restore(account_name, location, resource_group, restore_timestamp, target_database_account_name, databases_to_restore=None):
    '''
    Create a new Azure Cosmos DB database account by restoring from an existing database account.
    '''
    return call_az("az cosmosdb restore", locals())

