from .... pyaz_utils import call_az

def show(resource_group, workspace_name):
    '''
    Get a SQL's auditing policy.
    '''
    return call_az("az synapse sql audit-policy show", locals())


def update(resource_group, workspace_name, actions=None, add=None, blob_auditing_policy_name=None, blob_storage_target_state=None, enable_azure_monitor=None, event_hub=None, event_hub_authorization_rule_id=None, event_hub_target_state=None, force_string=None, log_analytics_target_state=None, log_analytics_workspace_resource_id=None, no_wait=None, queue_delay_time=None, remove=None, retention_days=None, set=None, state=None, storage_account=None, storage_endpoint=None, storage_key=None, storage_subscription=None, use_secondary_key=None):
    '''
    Update a SQL's auditing policy.
    '''
    return call_az("az synapse sql audit-policy update", locals())


def wait(blob_auditing_policy_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition is met.
    '''
    return call_az("az synapse sql audit-policy wait", locals())

