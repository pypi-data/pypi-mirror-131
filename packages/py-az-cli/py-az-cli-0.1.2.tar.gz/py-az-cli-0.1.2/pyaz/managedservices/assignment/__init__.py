from ... pyaz_utils import call_az

def create(definition, assignment_id=None, resource_group=None):
    '''
    Creates a new registration assignment.
    '''
    return call_az("az managedservices assignment create", locals())


def show(assignment, include_definition=None, resource_group=None):
    '''
    Gets a registration assignment.
    '''
    return call_az("az managedservices assignment show", locals())


def delete(assignment, resource_group=None):
    '''
    Deletes the registration assignment.
    '''
    return call_az("az managedservices assignment delete", locals())


def list(include_definition=None, resource_group=None):
    '''
    List all the registration assignments.
    '''
    return call_az("az managedservices assignment list", locals())

