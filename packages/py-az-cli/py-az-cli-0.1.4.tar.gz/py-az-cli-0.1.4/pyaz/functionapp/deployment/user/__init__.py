from .... pyaz_utils import _call_az

def set(user_name, password=None):
    '''
    Update deployment credentials.
    '''
    return _call_az("az functionapp deployment user set", locals())


def show():
    return _call_az("az functionapp deployment user show", locals())

