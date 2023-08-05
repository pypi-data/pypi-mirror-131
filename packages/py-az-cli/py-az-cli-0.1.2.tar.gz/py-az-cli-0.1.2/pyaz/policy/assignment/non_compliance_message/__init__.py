from .... pyaz_utils import call_az

def create(message, name, policy_definition_reference_id=None, resource_group=None, scope=None):
    '''
    Add a non-compliance message to a policy assignment.
    '''
    return call_az("az policy assignment non-compliance-message create", locals())


def list(name, resource_group=None, scope=None):
    '''
    List the non-compliance messages for a policy assignment.
    '''
    return call_az("az policy assignment non-compliance-message list", locals())


def delete(message, name, policy_definition_reference_id=None, resource_group=None, scope=None):
    '''
    Remove one or more non-compliance messages from a policy assignment.
    '''
    return call_az("az policy assignment non-compliance-message delete", locals())

