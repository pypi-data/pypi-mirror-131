from ... pyaz_utils import call_az

def create(name, registry, count=None, no_wait=None, os=None, resource_group=None, subnet_id=None, tier=None):
    '''
    Create an agent pool for an Azure Container Registry.
    '''
    return call_az("az acr agentpool create", locals())


def update(name, registry, count=None, no_wait=None, resource_group=None):
    '''
    Update an agent pool for an Azure Container Registry.
    '''
    return call_az("az acr agentpool update", locals())


def delete(name, registry, no_wait=None, resource_group=None, yes=None):
    '''
    Delete an agent pool.
    '''
    return call_az("az acr agentpool delete", locals())


def list(registry, resource_group=None):
    '''
    List the agent pools for an Azure Container Registry.
    '''
    return call_az("az acr agentpool list", locals())


def show(name, registry, queue_count=None, resource_group=None):
    '''
    Get the properties of a specified agent pool for an Azure Container Registry.
    '''
    return call_az("az acr agentpool show", locals())

