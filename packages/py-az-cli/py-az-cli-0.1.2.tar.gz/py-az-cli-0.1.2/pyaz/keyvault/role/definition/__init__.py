from .... pyaz_utils import call_az

def list(custom_role_only=None, hsm_name=None, scope=None):
    return call_az("az keyvault role definition list", locals())


def create(hsm_name, role_definition):
    '''
    Create a custom role definition.
    '''
    return call_az("az keyvault role definition create", locals())


def update(hsm_name, role_definition):
    '''
    Update a role definition.
    '''
    return call_az("az keyvault role definition update", locals())


def delete(hsm_name, name=None, role_id=None):
    '''
    Delete a role definition.
    '''
    return call_az("az keyvault role definition delete", locals())


def show(hsm_name, name=None, role_id=None):
    '''
    Show the details of a role definition.
    '''
    return call_az("az keyvault role definition show", locals())

