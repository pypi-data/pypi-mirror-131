from .... pyaz_utils import call_az

def set(name, resource_group, docker_custom_image_name=None, docker_registry_server_password=None, docker_registry_server_url=None, docker_registry_server_user=None, slot=None):
    '''
    Set an existing function app's container settings.
    '''
    return call_az("az functionapp config container set", locals())


def delete(name, resource_group, slot=None):
    '''
    Delete an existing function app's container settings.
    '''
    return call_az("az functionapp config container delete", locals())


def show(name, resource_group, slot=None):
    '''
    Get details of a function app's container settings.
    '''
    return call_az("az functionapp config container show", locals())

