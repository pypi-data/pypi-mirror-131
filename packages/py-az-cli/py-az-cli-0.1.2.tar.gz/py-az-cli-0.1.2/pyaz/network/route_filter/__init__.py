from ... pyaz_utils import call_az
from . import rule


def create(name, resource_group, location=None, tags=None):
    '''
    Create a route filter.
    '''
    return call_az("az network route-filter create", locals())


def list(resource_group=None):
    '''
    List route filters.
    '''
    return call_az("az network route-filter list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a route filter.
    '''
    return call_az("az network route-filter show", locals())


def delete(name, resource_group):
    '''
    Delete a route filter.
    '''
    return call_az("az network route-filter delete", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a route filter.
    '''
    return call_az("az network route-filter update", locals())

