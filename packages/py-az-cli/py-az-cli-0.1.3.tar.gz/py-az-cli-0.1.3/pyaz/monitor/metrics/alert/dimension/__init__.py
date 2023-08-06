from ..... pyaz_utils import _call_az

def create(name, value, operator=None):
    '''
    Build a metric alert rule dimension.
    '''
    return _call_az("az monitor metrics alert dimension create", locals())

