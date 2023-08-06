from .... pyaz_utils import _call_az

def show():
    '''
    Get deployment publishing user.
    '''
    return _call_az("az webapp deployment user show", locals())


def set(user_name, password=None):
    '''
    Update deployment credentials.
    '''
    return _call_az("az webapp deployment user set", locals())

