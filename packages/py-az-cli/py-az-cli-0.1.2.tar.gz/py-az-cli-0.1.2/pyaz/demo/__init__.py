from .. pyaz_utils import call_az

def style(theme=None):
    '''
    A demo showing supported text styles.
    '''
    return call_az("az demo style", locals())

