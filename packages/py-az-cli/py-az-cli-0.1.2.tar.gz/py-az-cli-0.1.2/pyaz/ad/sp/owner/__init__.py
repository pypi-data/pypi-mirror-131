from .... pyaz_utils import call_az

def list(id):
    '''
    List service principal owners.
    '''
    return call_az("az ad sp owner list", locals())

