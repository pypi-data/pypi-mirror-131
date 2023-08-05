from .... pyaz_utils import call_az

def list(name, resource_group, slot=None):
    '''
    Get a web app's connection strings.
    '''
    return call_az("az webapp config connection-string list", locals())


def set(connection_string_type, name, resource_group, settings=None, slot=None, slot_settings=None):
    '''
    Update a web app's connection strings.
    '''
    return call_az("az webapp config connection-string set", locals())


def delete(name, resource_group, setting_names, slot=None):
    '''
    Delete a web app's connection strings.
    '''
    return call_az("az webapp config connection-string delete", locals())

