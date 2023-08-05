from ..... pyaz_utils import call_az

def create(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, consumer_group=None, data_format=None, event_system_properties=None, iot_hub_resource_id=None, location=None, mapping_rule_name=None, no_wait=None, shared_access_policy_name=None, table_name=None):
    '''
    Create a data connection.
    '''
    return call_az("az synapse kusto data-connection iot-hub create", locals())


def update(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, consumer_group=None, data_format=None, event_system_properties=None, iot_hub_resource_id=None, location=None, mapping_rule_name=None, no_wait=None, shared_access_policy_name=None, table_name=None):
    '''
    Updates a data connection.
    '''
    return call_az("az synapse kusto data-connection iot-hub update", locals())

