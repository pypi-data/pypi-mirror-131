from .... pyaz_utils import _call_az

def list(id):
    '''
    List service principal owners.
    '''
    return _call_az("az ad sp owner list", locals())

