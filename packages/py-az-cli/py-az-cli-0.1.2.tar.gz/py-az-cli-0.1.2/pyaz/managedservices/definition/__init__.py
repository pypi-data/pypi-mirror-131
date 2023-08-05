from ... pyaz_utils import call_az

def create(name, principal_id, role_definition_id, tenant_id, definition_id=None, description=None, plan_name=None, plan_product=None, plan_publisher=None, plan_version=None):
    '''
    Creates a new registration definition.
    '''
    return call_az("az managedservices definition create", locals())


def list():
    '''
    List all the registration definitions under the default scope or under the subscription provided.
    '''
    return call_az("az managedservices definition list", locals())


def delete(definition):
    '''
    Deletes a registration.
    '''
    return call_az("az managedservices definition delete", locals())


def show(definition):
    '''
    Gets a registration definition.
    '''
    return call_az("az managedservices definition show", locals())

