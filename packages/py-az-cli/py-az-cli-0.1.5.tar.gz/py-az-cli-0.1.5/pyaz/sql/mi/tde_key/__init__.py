from .... pyaz_utils import _call_az

def show(managed_instance, resource_group):
    return _call_az("az sql mi tde-key show", locals())


def set(managed_instance, resource_group, server_key_type, auto_rotation_enabled=None, kid=None):
    '''
    Sets the SQL Instance's encryption protector.
    '''
    return _call_az("az sql mi tde-key set", locals())

