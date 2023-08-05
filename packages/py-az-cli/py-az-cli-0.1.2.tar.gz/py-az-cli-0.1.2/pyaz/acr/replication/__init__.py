from ... pyaz_utils import call_az

def list(registry, resource_group=None):
    '''
    List all of the regions for a geo-replicated Azure Container Registry.
    '''
    return call_az("az acr replication list", locals())


def create(location, registry, name=None, region_endpoint_enabled=None, resource_group=None, tags=None, zone_redundancy=None):
    '''
    Create a replicated region for an Azure Container Registry.
    '''
    return call_az("az acr replication create", locals())


def delete(name, registry, resource_group=None):
    '''
    Delete a replicated region from an Azure Container Registry.
    '''
    return call_az("az acr replication delete", locals())


def show(name, registry, resource_group=None):
    '''
    Get the details of a replicated region.
    '''
    return call_az("az acr replication show", locals())


def update(name, registry, add=None, force_string=None, region_endpoint_enabled=None, remove=None, resource_group=None, set=None, tags=None):
    '''
    Updates a replication.
    '''
    return call_az("az acr replication update", locals())

