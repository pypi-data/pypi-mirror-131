from ..... pyaz_utils import call_az

def create(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, compression=None, consumer_group=None, data_format=None, event_hub_resource_id=None, event_system_properties=None, location=None, managed_identity_resource_id=None, mapping_rule_name=None, no_wait=None, table_name=None):
    '''
    Create a data connection.
    '''
    return call_az("az synapse kusto data-connection event-hub create", locals())


def update(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, compression=None, consumer_group=None, data_format=None, event_hub_resource_id=None, event_system_properties=None, location=None, managed_identity_resource_id=None, mapping_rule_name=None, no_wait=None, table_name=None):
    '''
    Updates a data connection.
    '''
    return call_az("az synapse kusto data-connection event-hub update", locals())

