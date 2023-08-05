from .... pyaz_utils import call_az

def show(registry, resource_group=None):
    '''
    Show the configured content-trust policy for an Azure Container Registry.
    '''
    return call_az("az acr config content-trust show", locals())


def update(registry, resource_group=None, status=None):
    '''
    Update content-trust policy for an Azure Container Registry.
    '''
    return call_az("az acr config content-trust update", locals())

