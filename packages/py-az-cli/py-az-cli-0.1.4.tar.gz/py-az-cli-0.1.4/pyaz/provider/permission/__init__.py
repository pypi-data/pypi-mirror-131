from ... pyaz_utils import _call_az

def list(namespace):
    '''
    List permissions from a provider.
    '''
    return _call_az("az provider permission list", locals())

