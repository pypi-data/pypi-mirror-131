from ... pyaz_utils import call_az

def list():
    '''
    List all security assessment results.
    '''
    return call_az("az security assessment list", locals())


def show(name, assessed_resource_id=None):
    '''
    Shows a security assessment.
    '''
    return call_az("az security assessment show", locals())


def create(name, status_code, additional_data=None, assessed_resource_id=None, status_cause=None, status_description=None):
    '''
    Creates a customer managed security assessment.
    '''
    return call_az("az security assessment create", locals())


def delete(name, assessed_resource_id=None):
    '''
    Deletes a security assessment.
    '''
    return call_az("az security assessment delete", locals())

