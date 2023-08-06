from ... pyaz_utils import _call_az

def list(name, resource_group=None):
    '''
    List app settings of the static app.
    '''
    return _call_az("az staticwebapp appsettings list", locals())


def set(name, setting_names, resource_group=None):
    '''
    Add to or change the app settings of the static app.
    '''
    return _call_az("az staticwebapp appsettings set", locals())


def delete(name, setting_names, resource_group=None):
    '''
    Delete app settings with given keys of the static app.
    '''
    return _call_az("az staticwebapp appsettings delete", locals())

