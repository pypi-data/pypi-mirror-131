from ... pyaz_utils import call_az

def list():
    '''
    Shows the Azure Security Center Home region location.
    '''
    return call_az("az security location list", locals())


def show(name):
    '''
    Shows the Azure Security Center Home region location.
    '''
    return call_az("az security location show", locals())

