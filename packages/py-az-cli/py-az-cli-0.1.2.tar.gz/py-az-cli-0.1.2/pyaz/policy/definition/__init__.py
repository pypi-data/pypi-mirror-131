from ... pyaz_utils import call_az

def create(name, description=None, display_name=None, management_group=None, metadata=None, mode=None, params=None, rules=None, subscription=None):
    '''
    Create a policy definition.
    '''
    return call_az("az policy definition create", locals())


def delete(name, management_group=None, subscription=None):
    '''
    Delete a policy definition.
    '''
    return call_az("az policy definition delete", locals())


def list(management_group=None, subscription=None):
    '''
    List policy definitions.
    '''
    return call_az("az policy definition list", locals())


def show(name, management_group=None, subscription=None):
    '''
    Show a policy definition.
    '''
    return call_az("az policy definition show", locals())


def update(name, description=None, display_name=None, management_group=None, metadata=None, mode=None, params=None, rules=None, subscription=None):
    '''
    Update a policy definition.
    '''
    return call_az("az policy definition update", locals())

