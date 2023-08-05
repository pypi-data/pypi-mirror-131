from ... pyaz_utils import call_az
from . import firewall_rule, key, managed_identity


def show(name, resource_group):
    '''
    Get a Synapse workspace.
    '''
    return call_az("az synapse workspace show", locals())


def list(resource_group=None):
    '''
    List all Synapse workspaces.
    '''
    return call_az("az synapse workspace list", locals())


def create(file_system, name, resource_group, sql_admin_login_password, sql_admin_login_user, storage_account, account_name=None, allowed_tenant_ids=None, collaboration_branch=None, enable_managed_vnet=None, host_name=None, key_identifier=None, key_name=None, location=None, no_wait=None, prevent_exfiltration=None, project_name=None, repository_name=None, repository_type=None, root_folder=None, tags=None, tenant_id=None):
    '''
    Create a Synapse workspace.
    '''
    return call_az("az synapse workspace create", locals())


def update(name, resource_group, account_name=None, allowed_tenant_ids=None, collaboration_branch=None, host_name=None, key_name=None, no_wait=None, project_name=None, repository_name=None, repository_type=None, root_folder=None, sql_admin_login_password=None, tags=None, tenant_id=None):
    '''
    Update a Synapse workspace.
    '''
    return call_az("az synapse workspace update", locals())


def check_name(name):
    '''
    Check if a Synapse workspace name is available or not.
    '''
    return call_az("az synapse workspace check-name", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a Synapse workspace.
    '''
    return call_az("az synapse workspace delete", locals())


def activate(key_identifier, name, resource_group, workspace_name, no_wait=None):
    '''
    Activates a workspace and change it's state from pending to success state when the workspace is first being provisioned and double encryption is enabled.
    '''
    return call_az("az synapse workspace activate", locals())


def wait(resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the workspace is met.
    '''
    return call_az("az synapse workspace wait", locals())

