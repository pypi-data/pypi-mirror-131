from ... pyaz_utils import _call_az

def list():
    '''
    List the external security solutions.
    '''
    return _call_az("az security external-security-solution list", locals())


def show(name, resource_group):
    '''
    Shows an external security solution.
    '''
    return _call_az("az security external-security-solution show", locals())

