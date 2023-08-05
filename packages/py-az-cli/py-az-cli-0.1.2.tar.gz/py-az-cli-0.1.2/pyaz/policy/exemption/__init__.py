from ... pyaz_utils import call_az

def create(name, description=None, display_name=None, exemption_category=None, expires_on=None, metadata=None, policy_assignment=None, policy_definition_reference_ids=None, resource_group=None, scope=None):
    '''
    Create a policy exemption.
    '''
    return call_az("az policy exemption create", locals())


def delete(name, resource_group=None, scope=None):
    '''
    Delete a policy exemption.
    '''
    return call_az("az policy exemption delete", locals())


def list(disable_scope_strict_match=None, resource_group=None, scope=None):
    '''
    List policy exemptions.
    '''
    return call_az("az policy exemption list", locals())


def show(name, resource_group=None, scope=None):
    '''
    Show a policy exemption.
    '''
    return call_az("az policy exemption show", locals())


def update(name, description=None, display_name=None, exemption_category=None, expires_on=None, metadata=None, policy_definition_reference_ids=None, resource_group=None, scope=None):
    '''
    Update a policy exemption.
    '''
    return call_az("az policy exemption update", locals())

