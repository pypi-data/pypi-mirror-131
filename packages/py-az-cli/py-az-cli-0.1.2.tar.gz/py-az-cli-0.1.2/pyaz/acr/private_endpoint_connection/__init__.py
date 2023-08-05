from ... pyaz_utils import call_az

def delete(name, registry_name, resource_group=None):
    '''
    Delete a private endpoint connection request for a container registry
    '''
    return call_az("az acr private-endpoint-connection delete", locals())


def show(name, registry_name, resource_group=None):
    '''
    Show details of a container registry's private endpoint connection
    '''
    return call_az("az acr private-endpoint-connection show", locals())


def list(registry_name, resource_group=None):
    '''
    List all private endpoint connections to a container registry
    '''
    return call_az("az acr private-endpoint-connection list", locals())


def approve(name, registry_name, description=None, resource_group=None):
    '''
    Approve a private endpoint connection request for a container registry
    '''
    return call_az("az acr private-endpoint-connection approve", locals())


def reject(name, registry_name, description=None, resource_group=None):
    '''
    Reject a private endpoint connection request for a container registry
    '''
    return call_az("az acr private-endpoint-connection reject", locals())

