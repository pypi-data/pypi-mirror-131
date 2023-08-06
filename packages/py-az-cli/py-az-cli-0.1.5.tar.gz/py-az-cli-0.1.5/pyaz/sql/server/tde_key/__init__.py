from .... pyaz_utils import _call_az

def show(resource_group, server):
    return _call_az("az sql server tde-key show", locals())


def set(resource_group, server, server_key_type, auto_rotation_enabled=None, kid=None):
    '''
    Sets the server's encryption protector.
    '''
    return _call_az("az sql server tde-key set", locals())

