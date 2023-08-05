from .... pyaz_utils import call_az

def list(kusto_pool_name, resource_group, workspace_name):
    '''
    Returns the list of attached database configurations of the given Kusto Pool.
    '''
    return call_az("az synapse kusto attached-database-configuration list", locals())


def show(attached_database_configuration_name, kusto_pool_name, resource_group, workspace_name):
    '''
    Returns an attached database configuration.
    '''
    return call_az("az synapse kusto attached-database-configuration show", locals())


def create(attached_database_configuration_name, kusto_pool_name, resource_group, workspace_name, database_name=None, default_principals_modification_kind=None, kusto_pool_resource_id=None, location=None, no_wait=None, table_level_sharing_properties=None):
    '''
    Create an attached database configuration.
    '''
    return call_az("az synapse kusto attached-database-configuration create", locals())


def update(attached_database_configuration_name, kusto_pool_name, resource_group, workspace_name, add=None, database_name=None, default_principals_modification_kind=None, force_string=None, kusto_pool_resource_id=None, location=None, no_wait=None, remove=None, set=None, table_level_sharing_properties=None):
    '''
    Update an attached database configuration.
    '''
    return call_az("az synapse kusto attached-database-configuration update", locals())


def delete(attached_database_configuration_name, kusto_pool_name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Deletes the attached database configuration with the given name.
    '''
    return call_az("az synapse kusto attached-database-configuration delete", locals())


def wait(attached_database_configuration_name, kusto_pool_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the synapse kusto attached-database-configuration is met.
    '''
    return call_az("az synapse kusto attached-database-configuration wait", locals())

