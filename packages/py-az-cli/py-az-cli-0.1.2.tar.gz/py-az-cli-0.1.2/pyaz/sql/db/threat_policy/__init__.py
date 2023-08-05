from .... pyaz_utils import call_az

def show(name, resource_group, server):
    return call_az("az sql db threat-policy show", locals())


def update(name, resource_group, server, add=None, disabled_alerts=None, email_account_admins=None, email_addresses=None, force_string=None, remove=None, retention_days=None, set=None, state=None, storage_account=None, storage_endpoint=None, storage_key=None):
    '''
    Update a database's threat detection policy.
    '''
    return call_az("az sql db threat-policy update", locals())

