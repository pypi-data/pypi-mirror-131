from ... pyaz_utils import call_az

def build(builder, image, registry, agent_pool=None, auth_mode=None, no_format=None, no_logs=None, no_wait=None, pack_image_tag=None, platform=None, pull=None, resource_group=None, timeout=None):
    '''
    Queues a quick build task that builds an app and pushes it into an Azure Container Registry.
    '''
    return call_az("az acr pack build", locals())

