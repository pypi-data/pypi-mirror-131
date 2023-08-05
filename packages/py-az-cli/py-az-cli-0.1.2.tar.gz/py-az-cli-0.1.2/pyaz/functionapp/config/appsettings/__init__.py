from .... pyaz_utils import call_az

def list(name, resource_group, slot=None):
    '''
    Show settings for a function app.
    '''
    return call_az("az functionapp config appsettings list", locals())


def set(name, resource_group, settings=None, slot=None, slot_settings=None):
    '''
    Update a function app's settings.
    '''
    return call_az("az functionapp config appsettings set", locals())


def delete(name, resource_group, setting_names, slot=None):
    '''
    Delete a function app's settings.
    '''
    return call_az("az functionapp config appsettings delete", locals())

