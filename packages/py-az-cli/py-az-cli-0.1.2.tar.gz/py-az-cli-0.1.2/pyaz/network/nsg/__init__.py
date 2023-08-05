from ... pyaz_utils import call_az
from . import rule


def delete(name, resource_group):
    '''
    Delete a network security group.
    '''
    return call_az("az network nsg delete", locals())


def show(name, resource_group, expand=None):
    '''
    Get information about a network security group.
    '''
    return call_az("az network nsg show", locals())


def list(resource_group=None):
    '''
    List network security groups.
    '''
    return call_az("az network nsg list", locals())


def create(name, resource_group, location=None, tags=None):
    '''
    Create a network security group.
    '''
    return call_az("az network nsg create", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a network security group.
    '''
    return call_az("az network nsg update", locals())

