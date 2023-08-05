from ... pyaz_utils import call_az

def list():
    '''
    List supported of secure score controls details and state for scope.
    '''
    return call_az("az security secure-score-controls list", locals())


def list_by_score(name):
    '''
    List supported of secure score controls details and state for selected score.
    '''
    return call_az("az security secure-score-controls list_by_score", locals())

