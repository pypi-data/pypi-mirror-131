from .... pyaz_utils import call_az

def create(role, workspace_name, assignee=None, assignee_object_id=None, assignee_principal_type=None, assignment_id=None, item=None, item_type=None, scope=None):
    '''
    Create a role assignment.
    '''
    return call_az("az synapse role assignment create", locals())


def list(workspace_name, assignee=None, assignee_object_id=None, item=None, item_type=None, role=None, scope=None):
    '''
    List role assignments.
    '''
    return call_az("az synapse role assignment list", locals())


def show(id, workspace_name):
    '''
    Get a role assignment by id.
    '''
    return call_az("az synapse role assignment show", locals())


def delete(workspace_name, assignee=None, assignee_object_id=None, ids=None, item=None, item_type=None, role=None, scope=None, yes=None):
    '''
    Delete role assignments of workspace.
    '''
    return call_az("az synapse role assignment delete", locals())

