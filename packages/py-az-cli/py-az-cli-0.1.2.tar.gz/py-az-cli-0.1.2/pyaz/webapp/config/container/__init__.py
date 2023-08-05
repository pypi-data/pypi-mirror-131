from .... pyaz_utils import call_az

def set(name, resource_group, docker_custom_image_name=None, docker_registry_server_password=None, docker_registry_server_url=None, docker_registry_server_user=None, enable_app_service_storage=None, multicontainer_config_file=None, multicontainer_config_type=None, slot=None):
    '''
    Set an existing web app's container settings.
    '''
    return call_az("az webapp config container set", locals())


def delete(name, resource_group, slot=None):
    '''
    Delete an existing web app's container settings.
    '''
    return call_az("az webapp config container delete", locals())


def show(name, resource_group, show_multicontainer_config=None, slot=None):
    '''
    Get details of a web app's container settings.
    '''
    return call_az("az webapp config container show", locals())

