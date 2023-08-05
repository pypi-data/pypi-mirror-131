from .... pyaz_utils import call_az

def set(function_name, key_name, name, resource_group, key_value=None, slot=None):
    '''
    Create or update a function key.
    '''
    return call_az("az functionapp function keys set", locals())


def list(function_name, name, resource_group, slot=None):
    '''
    List all function keys.
    '''
    return call_az("az functionapp function keys list", locals())


def delete(key_name, name, resource_group, function_name=None, slot=None):
    '''
    Delete a function key.
    '''
    return call_az("az functionapp function keys delete", locals())

