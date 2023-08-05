from ..... pyaz_utils import call_az

def show(name, resource_group):
    return call_az("az sql server ms-support audit-policy show", locals())


def update(name, resource_group, add=None, blob_storage_target_state=None, event_hub=None, event_hub_authorization_rule_id=None, event_hub_target_state=None, force_string=None, log_analytics_target_state=None, log_analytics_workspace_resource_id=None, no_wait=None, remove=None, set=None, state=None, storage_account=None, storage_endpoint=None, storage_key=None):
    '''
    Update a server's Microsoft support operations auditing policy.
    '''
    return call_az("az sql server ms-support audit-policy update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the server's Microsoft support operations audit policy is met.
    '''
    return call_az("az sql server ms-support audit-policy wait", locals())

