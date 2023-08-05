from ... pyaz_utils import call_az

def list():
    '''
    Get details of secure score control definitions.
    '''
    return call_az("az security secure-score-control-definitions list", locals())

