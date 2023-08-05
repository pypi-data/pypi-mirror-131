from ... pyaz_utils import call_az

def create(definitions, name, definition_groups=None, description=None, display_name=None, management_group=None, metadata=None, params=None, subscription=None):
    '''
    Create a policy set definition.
    '''
    return call_az("az policy set-definition create", locals())


def delete(name, management_group=None, subscription=None):
    '''
    Delete a policy set definition.
    '''
    return call_az("az policy set-definition delete", locals())


def list(management_group=None, subscription=None):
    '''
    List policy set definitions.
    '''
    return call_az("az policy set-definition list", locals())


def show(name, management_group=None, subscription=None):
    '''
    Show a policy set definition.
    '''
    return call_az("az policy set-definition show", locals())


def update(name, definition_groups=None, definitions=None, description=None, display_name=None, management_group=None, metadata=None, params=None, subscription=None):
    '''
    Update a policy set definition.
    '''
    return call_az("az policy set-definition update", locals())

