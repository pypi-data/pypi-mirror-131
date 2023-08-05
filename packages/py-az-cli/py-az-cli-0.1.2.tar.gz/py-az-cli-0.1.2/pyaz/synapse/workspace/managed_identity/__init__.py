from .... pyaz_utils import call_az

def show_sql_access(resource_group, workspace_name):
    '''
    Show workspace's sql-access state to managed-identity.
    '''
    return call_az("az synapse workspace managed-identity show-sql-access", locals())


def grant_sql_access(resource_group, workspace_name, no_wait=None):
    '''
    Grant workspace's sql-access to managed-identity.
    '''
    return call_az("az synapse workspace managed-identity grant-sql-access", locals())


def revoke_sql_access(resource_group, workspace_name, no_wait=None):
    '''
    Revoke workspace's sql-access to managed-identity.
    '''
    return call_az("az synapse workspace managed-identity revoke-sql-access", locals())


def wait(resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of sql-access state to managed-identity is met.
    '''
    return call_az("az synapse workspace managed-identity wait", locals())

