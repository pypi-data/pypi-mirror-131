from ... pyaz_utils import call_az

def list(registry, resource_group=None):
    '''
    List all of the webhooks for an Azure Container Registry.
    '''
    return call_az("az acr webhook list", locals())


def create(actions, name, registry, uri, headers=None, location=None, resource_group=None, scope=None, status=None, tags=None):
    '''
    Create a webhook for an Azure Container Registry.
    '''
    return call_az("az acr webhook create", locals())


def delete(name, registry, resource_group=None):
    '''
    Delete a webhook from an Azure Container Registry.
    '''
    return call_az("az acr webhook delete", locals())


def show(name, registry, resource_group=None):
    '''
    Get the details of a webhook.
    '''
    return call_az("az acr webhook show", locals())


def get_config(name, registry, resource_group=None):
    '''
    Get the service URI and custom headers for the webhook.
    '''
    return call_az("az acr webhook get-config", locals())


def list_events(name, registry, resource_group=None):
    '''
    List recent events for a webhook.
    '''
    return call_az("az acr webhook list-events", locals())


def ping(name, registry, resource_group=None):
    '''
    Trigger a ping event for a webhook.
    '''
    return call_az("az acr webhook ping", locals())


def update(name, registry, actions=None, add=None, force_string=None, headers=None, remove=None, resource_group=None, scope=None, set=None, status=None, tags=None, uri=None):
    '''
    Update a webhook.
    '''
    return call_az("az acr webhook update", locals())

