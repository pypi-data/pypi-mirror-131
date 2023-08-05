from ..... pyaz_utils import call_az

def show(name, resource_group, security_alert_policy_name, workspace_name):
    '''
    Get a SQL pool's threat detection policy.
    '''
    return call_az("az synapse sql pool threat-policy show", locals())


def update(name, resource_group, workspace_name, add=None, disabled_alerts=None, email_account_admins=None, email_addresses=None, force_string=None, remove=None, retention_days=None, security_alert_policy_name=None, set=None, state=None, storage_account=None, storage_endpoint=None, storage_key=None):
    '''
    Update a SQL pool's threat detection policy.
    '''
    return call_az("az synapse sql pool threat-policy update", locals())

