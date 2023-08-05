from ... pyaz_utils import call_az
from . import credential, owner, permission


def create(display_name, app_roles=None, available_to_other_tenants=None, credential_description=None, end_date=None, homepage=None, identifier_uris=None, key_type=None, key_usage=None, key_value=None, native_app=None, oauth2_allow_implicit_flow=None, optional_claims=None, password=None, reply_urls=None, required_resource_accesses=None, start_date=None):
    '''
    Create a web application, web API or native application
    '''
    return call_az("az ad app create", locals())


def delete(id):
    '''
    Delete an application.
    '''
    return call_az("az ad app delete", locals())


def list(all=None, app_id=None, display_name=None, filter=None, identifier_uri=None, show_mine=None):
    '''
    List applications.
    '''
    return call_az("az ad app list", locals())


def show(id):
    '''
    Get the details of an application.
    '''
    return call_az("az ad app show", locals())


def update(id, add=None, app_roles=None, available_to_other_tenants=None, credential_description=None, display_name=None, end_date=None, force_string=None, homepage=None, identifier_uris=None, key_type=None, key_usage=None, key_value=None, oauth2_allow_implicit_flow=None, optional_claims=None, password=None, remove=None, reply_urls=None, required_resource_accesses=None, set=None, start_date=None):
    '''
    Update an application.
    '''
    return call_az("az ad app update", locals())

