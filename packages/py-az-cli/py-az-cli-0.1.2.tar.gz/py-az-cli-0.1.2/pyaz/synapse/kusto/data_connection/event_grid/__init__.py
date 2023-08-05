from ..... pyaz_utils import call_az

def create(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, blob_storage_event_type=None, consumer_group=None, data_format=None, event_hub_resource_id=None, ignore_first_record=None, location=None, mapping_rule_name=None, no_wait=None, storage_account_resource_id=None, table_name=None):
    '''
    Create a data connection.
    '''
    return call_az("az synapse kusto data-connection event-grid create", locals())


def update(data_connection_name, database_name, kusto_pool_name, resource_group, workspace_name, blob_storage_event_type=None, consumer_group=None, data_format=None, event_hub_resource_id=None, ignore_first_record=None, location=None, mapping_rule_name=None, no_wait=None, storage_account_resource_id=None, table_name=None):
    '''
    Updates a data connection.
    '''
    return call_az("az synapse kusto data-connection event-grid update", locals())

