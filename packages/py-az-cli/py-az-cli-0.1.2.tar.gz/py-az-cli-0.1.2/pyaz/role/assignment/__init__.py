from ... pyaz_utils import call_az

def delete(assignee=None, ids=None, include_inherited=None, resource_group=None, role=None, scope=None, yes=None):
    '''
    Delete role assignments.
    '''
    return call_az("az role assignment delete", locals())


def list(all=None, assignee=None, include_classic_administrators=None, include_groups=None, include_inherited=None, resource_group=None, role=None, scope=None):
    '''
    List role assignments.
    '''
    return call_az("az role assignment list", locals())


def create(role, assignee=None, assignee_object_id=None, assignee_principal_type=None, condition=None, condition_version=None, description=None, resource_group=None, scope=None):
    '''
    Create a new role assignment for a user, group, or service principal.
    '''
    return call_az("az role assignment create", locals())


def update(role_assignment):
    '''
    Update an existing role assignment for a user, group, or service principal.
    '''
    return call_az("az role assignment update", locals())


def list_changelogs(end_time=None, start_time=None):
    '''
    List changelogs for role assignments.
    '''
    return call_az("az role assignment list-changelogs", locals())

