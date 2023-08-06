from ... pyaz_utils import _call_az

def list(location=None, resource_group=None):
    '''
    List security alerts.
    '''
    return _call_az("az security alert list", locals())


def show(location, name, resource_group=None):
    '''
    Shows a security alert.
    '''
    return _call_az("az security alert show", locals())


def update(location, name, status, resource_group=None):
    '''
    Updates a security alert status.
    '''
    return _call_az("az security alert update", locals())

