from ... pyaz_utils import call_az

def list():
    '''
    List all security assessment results.
    '''
    return call_az("az security assessment-metadata list", locals())


def show(name):
    '''
    Shows a security assessment.
    '''
    return call_az("az security assessment-metadata show", locals())


def create(description, display_name, name, severity, remediation_description=None):
    '''
    Creates a customer managed security assessment type.
    '''
    return call_az("az security assessment-metadata create", locals())


def delete(name):
    '''
    Deletes a security assessment type and all it's assessment results.
    '''
    return call_az("az security assessment-metadata delete", locals())

