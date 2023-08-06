from ... pyaz_utils import _call_az

def list():
    '''
    List all security assessment results.
    '''
    return _call_az("az security assessment-metadata list", locals())


def show(name):
    '''
    Shows a security assessment.
    '''
    return _call_az("az security assessment-metadata show", locals())


def create(description, display_name, name, severity, remediation_description=None):
    '''
    Creates a customer managed security assessment type.
    '''
    return _call_az("az security assessment-metadata create", locals())


def delete(name):
    '''
    Deletes a security assessment type and all it's assessment results.
    '''
    return _call_az("az security assessment-metadata delete", locals())

