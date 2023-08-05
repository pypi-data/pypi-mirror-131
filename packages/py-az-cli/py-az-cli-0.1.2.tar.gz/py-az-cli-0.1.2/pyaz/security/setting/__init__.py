from ... pyaz_utils import call_az

def list():
    '''
    List security settings.
    '''
    return call_az("az security setting list", locals())


def show(name):
    '''
    Shows a security setting.
    '''
    return call_az("az security setting show", locals())


def update(enabled, name):
    '''
    Updates a security setting.
    '''
    return call_az("az security setting update", locals())

