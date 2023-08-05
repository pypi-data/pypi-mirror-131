from ... pyaz_utils import call_az

def list(top=None):
    '''
    List policy metadata resources.
    '''
    return call_az("az policy metadata list", locals())


def show(name):
    '''
    Get a single policy metadata resource.
    '''
    return call_az("az policy metadata show", locals())

