from ... pyaz_utils import _call_az

def list(control_name, standard_name):
    '''
    Get details and state of assessments mapped to selected regulatory compliance control.
    '''
    return _call_az("az security regulatory-compliance-assessments list", locals())


def show(control_name, name, standard_name):
    '''
    Shows supported regulatory compliance details and state for selected assessment.
    '''
    return _call_az("az security regulatory-compliance-assessments show", locals())

