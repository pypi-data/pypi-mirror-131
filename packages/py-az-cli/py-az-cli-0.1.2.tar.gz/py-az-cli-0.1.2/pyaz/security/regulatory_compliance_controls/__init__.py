from ... pyaz_utils import call_az

def list(standard_name):
    '''
    List supported of regulatory compliance controls details and state for selected standard.
    '''
    return call_az("az security regulatory-compliance-controls list", locals())


def show(name, standard_name):
    '''
    Shows a regulatory compliance details state for selected standard.
    '''
    return call_az("az security regulatory-compliance-controls show", locals())

