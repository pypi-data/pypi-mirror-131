from .... pyaz_utils import call_az

def list(database_name, kusto_pool_name, resource_group, workspace_name):
    '''
    Lists all Kusto pool database principalAssignments.
    '''
    return call_az("az synapse kusto database-principal-assignment list", locals())


def show(database_name, kusto_pool_name, principal_assignment_name, resource_group, workspace_name):
    '''
    Gets a Kusto pool database principalAssignment.
    '''
    return call_az("az synapse kusto database-principal-assignment show", locals())


def create(database_name, kusto_pool_name, principal_assignment_name, resource_group, workspace_name, no_wait=None, principal_id=None, principal_type=None, role=None, tenant_id=None):
    '''
    Creates a Kusto pool database principalAssignment.
    '''
    return call_az("az synapse kusto database-principal-assignment create", locals())


def update(database_name, kusto_pool_name, principal_assignment_name, resource_group, workspace_name, add=None, force_string=None, no_wait=None, principal_id=None, principal_type=None, remove=None, role=None, set=None, tenant_id=None):
    '''
    Update a Kusto pool database principalAssignment.
    '''
    return call_az("az synapse kusto database-principal-assignment update", locals())


def delete(database_name, kusto_pool_name, principal_assignment_name, resource_group, workspace_name, no_wait=None, yes=None):
    '''
    Deletes a Kusto pool principalAssignment.
    '''
    return call_az("az synapse kusto database-principal-assignment delete", locals())


def wait(database_name, kusto_pool_name, principal_assignment_name, resource_group, workspace_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the synapse kusto database-principal-assignment is met.
    '''
    return call_az("az synapse kusto database-principal-assignment wait", locals())

