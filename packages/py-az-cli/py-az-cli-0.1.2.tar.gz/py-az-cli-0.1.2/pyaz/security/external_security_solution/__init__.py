from ... pyaz_utils import call_az

def list():
    '''
    List the external security solutions.
    '''
    return call_az("az security external-security-solution list", locals())


def show(name, resource_group):
    '''
    Shows an external security solution.
    '''
    return call_az("az security external-security-solution show", locals())

