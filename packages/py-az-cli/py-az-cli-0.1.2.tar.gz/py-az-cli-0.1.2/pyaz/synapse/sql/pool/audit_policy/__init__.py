from ..... pyaz_utils import call_az

def show(name, resource_group, workspace_name):
    '''
    Get a SQL pool's auditing policy.
    '''
    return call_az("az synapse sql pool audit-policy show", locals())


def update(name, resource_group, workspace_name, actions=None, add=None, blob_storage_target_state=None, enable_azure_monitor=None, event_hub=None, event_hub_authorization_rule_id=None, event_hub_target_state=None, force_string=None, log_analytics_target_state=None, log_analytics_workspace_resource_id=None, remove=None, retention_days=None, set=None, state=None, storage_account=None, storage_endpoint=None, storage_key=None, storage_subscription=None, use_secondary_key=None):
    '''
    Update a SQL pool's auditing policy.
    '''
    return call_az("az synapse sql pool audit-policy update", locals())

