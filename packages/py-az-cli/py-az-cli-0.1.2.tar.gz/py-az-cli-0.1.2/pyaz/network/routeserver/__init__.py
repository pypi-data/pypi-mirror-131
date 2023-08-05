from ... pyaz_utils import call_az
from . import peering


def create(hosted_subnet, name, resource_group, location=None, public_ip_address=None, tags=None):
    '''
    Create a route server.
    '''
    return call_az("az network routeserver create", locals())


def update(name, resource_group, add=None, allow_b2b_traffic=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update a route server.
    '''
    return call_az("az network routeserver update", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a route server under a resource group.
    '''
    return call_az("az network routeserver delete", locals())


def show(name, resource_group):
    '''
    Show a route server.
    '''
    return call_az("az network routeserver show", locals())


def list(resource_group=None):
    '''
    List all route servers under a subscription or a resource group.
    '''
    return call_az("az network routeserver list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the route server is met.
    '''
    return call_az("az network routeserver wait", locals())

