from .... pyaz_utils import call_az

def set(user_name, password=None):
    '''
    Update deployment credentials.
    '''
    return call_az("az functionapp deployment user set", locals())


def show():
    return call_az("az functionapp deployment user show", locals())

