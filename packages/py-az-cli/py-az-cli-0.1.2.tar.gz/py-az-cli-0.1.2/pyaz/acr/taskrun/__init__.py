from ... pyaz_utils import call_az

def list(registry, resource_group=None):
    '''
    List the taskruns for an Azure Container Registry.
    '''
    return call_az("az acr taskrun list", locals())


def delete(name, registry, resource_group=None, yes=None):
    '''
    Delete a taskrun from an Azure Container Registry.
    '''
    return call_az("az acr taskrun delete", locals())


def show(name, registry, resource_group=None):
    '''
    Get the properties of a named taskrun for an Azure Container Registry.
    '''
    return call_az("az acr taskrun show", locals())


def logs(name, registry, resource_group=None):
    '''
    Show run logs for a particular taskrun.
    '''
    return call_az("az acr taskrun logs", locals())

