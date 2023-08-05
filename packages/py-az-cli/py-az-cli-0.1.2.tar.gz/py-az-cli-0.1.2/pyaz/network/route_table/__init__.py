from ... pyaz_utils import call_az
from . import route


def create(name, resource_group, disable_bgp_route_propagation=None, location=None, tags=None):
    '''
    Create a route table.
    '''
    return call_az("az network route-table create", locals())


def delete(name, resource_group):
    '''
    Delete a route table.
    '''
    return call_az("az network route-table delete", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a route table.
    '''
    return call_az("az network route-table show", locals())


def list(resource_group=None):
    '''
    List route tables.
    '''
    return call_az("az network route-table list", locals())


def update(name, resource_group, add=None, disable_bgp_route_propagation=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update a route table.
    '''
    return call_az("az network route-table update", locals())

