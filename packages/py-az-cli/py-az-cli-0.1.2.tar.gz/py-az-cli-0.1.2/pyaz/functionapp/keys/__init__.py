from ... pyaz_utils import call_az

def set(key_name, key_type, name, resource_group, key_value=None, slot=None):
    '''
    Create or update a function app key.
    '''
    return call_az("az functionapp keys set", locals())


def list(name, resource_group, slot=None):
    '''
    List all function app keys.
    '''
    return call_az("az functionapp keys list", locals())


def delete(key_name, key_type, name, resource_group, slot=None):
    '''
    Delete a function app key.
    '''
    return call_az("az functionapp keys delete", locals())

