from ... pyaz_utils import _call_az

def list():
    '''
    Adaptive Application Controls - List
    '''
    return _call_az("az security adaptive-application-controls list", locals())


def show(group_name):
    '''
    Adaptive Application Controls - Get
    '''
    return _call_az("az security adaptive-application-controls show", locals())

