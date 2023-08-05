from ... pyaz_utils import call_az
from . import subscription


def list(no_register=None):
    '''
    List all management groups.
    '''
    return call_az("az account management-group list", locals())


def show(name, expand=None, no_register=None, recurse=None):
    '''
    Get a specific management group.
    '''
    return call_az("az account management-group show", locals())


def create(name, display_name=None, no_register=None, parent=None):
    '''
    Create a new management group.
    '''
    return call_az("az account management-group create", locals())


def delete(name, no_register=None):
    '''
    Delete an existing management group.
    '''
    return call_az("az account management-group delete", locals())


def update(name, add=None, display_name=None, force_string=None, parent=None, remove=None, set=None):
    '''
    Update an existing management group.
    '''
    return call_az("az account management-group update", locals())

