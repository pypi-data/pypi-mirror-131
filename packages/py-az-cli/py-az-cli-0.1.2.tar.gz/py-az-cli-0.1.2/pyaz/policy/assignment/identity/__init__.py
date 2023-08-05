from .... pyaz_utils import call_az

def assign(name, identity_scope=None, resource_group=None, role=None, scope=None, system_assigned=None, user_assigned=None):
    '''
    Add a system assigned identity or a user assigned identity to a policy assignment.
    '''
    return call_az("az policy assignment identity assign", locals())


def show(name, resource_group=None, scope=None):
    '''
    Show a policy assignment's managed identity.
    '''
    return call_az("az policy assignment identity show", locals())


def remove(name, resource_group=None, scope=None):
    '''
    Remove a managed identity from a policy assignment.
    '''
    return call_az("az policy assignment identity remove", locals())

