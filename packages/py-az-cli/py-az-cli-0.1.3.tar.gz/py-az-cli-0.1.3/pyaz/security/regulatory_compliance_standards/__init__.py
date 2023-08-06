from ... pyaz_utils import _call_az

def list():
    '''
    List supported regulatory compliance standards details and state results.
    '''
    return _call_az("az security regulatory-compliance-standards list", locals())


def show(name):
    '''
    Shows a regulatory compliance details state for selected standard.
    '''
    return _call_az("az security regulatory-compliance-standards show", locals())

