from .. pyaz_utils import _call_az

def style(theme=None):
    '''
    A demo showing supported text styles.
    '''
    return _call_az("az demo style", locals())

