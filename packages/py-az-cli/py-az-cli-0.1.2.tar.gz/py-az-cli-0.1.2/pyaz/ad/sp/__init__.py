from ... pyaz_utils import call_az
from . import credential, owner


def create(id):
    '''
    Create a service principal.
    '''
    return call_az("az ad sp create", locals())


def delete(id):
    '''
    Delete a service principal and its role assignments.
    '''
    return call_az("az ad sp delete", locals())


def list(all=None, display_name=None, filter=None, show_mine=None, spn=None):
    '''
    List service principals.
    '''
    return call_az("az ad sp list", locals())


def show(id):
    '''
    Get the details of a service principal.
    '''
    return call_az("az ad sp show", locals())


def update(id, add=None, force_string=None, remove=None, set=None):
    '''
    Update a service principal
    '''
    return call_az("az ad sp update", locals())


def create_for_rbac(cert=None, create_cert=None, keyvault=None, name=None, role=None, scopes=None, sdk_auth=None, skip_assignment=None, years=None):
    '''
    Create a service principal and configure its access to Azure resources.
    '''
    return call_az("az ad sp create-for-rbac", locals())

