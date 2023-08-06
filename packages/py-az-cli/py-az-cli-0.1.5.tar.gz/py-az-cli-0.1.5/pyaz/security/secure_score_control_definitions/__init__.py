from ... pyaz_utils import _call_az

def list():
    '''
    Get details of secure score control definitions.
    '''
    return _call_az("az security secure-score-control-definitions list", locals())

