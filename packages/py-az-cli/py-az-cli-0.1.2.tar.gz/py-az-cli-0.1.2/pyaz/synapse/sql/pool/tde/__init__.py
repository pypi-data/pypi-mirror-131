from ..... pyaz_utils import call_az

def set(name, resource_group, status, transparent_data_encryption_name, workspace_name):
    '''
    Set a SQL pool's transparent data encryption configuration.
    '''
    return call_az("az synapse sql pool tde set", locals())


def show(name, resource_group, transparent_data_encryption_name, workspace_name):
    '''
    Get a SQL pool's transparent data encryption configuration.
    '''
    return call_az("az synapse sql pool tde show", locals())

