from ... pyaz_utils import call_az
from . import operation, release, revision, versionset


def import_(path, resource_group, service_name, specification_format, api_id=None, api_revision=None, api_type=None, api_version=None, api_version_set_id=None, description=None, display_name=None, no_wait=None, protocols=None, service_url=None, soap_api_type=None, specification_path=None, specification_url=None, subscription_key_header_name=None, subscription_key_query_param_name=None, subscription_required=None, wsdl_endpoint_name=None, wsdl_service_name=None):
    '''
    Import an API Management API.
    '''
    return call_az("az apim api import", locals())


def create(api_id, display_name, path, resource_group, service_name, api_type=None, authorization_scope=None, authorization_server_id=None, bearer_token_sending_methods=None, description=None, no_wait=None, open_id_provider_id=None, protocols=None, service_url=None, subscription_key_header_name=None, subscription_key_query_param_name=None, subscription_key_required=None, subscription_required=None):
    '''
    Create an API Management API.
    '''
    return call_az("az apim api create", locals())


def show(api_id, resource_group, service_name):
    '''
    Show details of an API Management API.
    '''
    return call_az("az apim api show", locals())


def list(resource_group, service_name, filter_display_name=None, skip=None, top=None):
    '''
    List API Management API's.
    '''
    return call_az("az apim api list", locals())


def delete(api_id, resource_group, service_name, delete_revisions=None, if_match=None, no_wait=None, yes=None):
    '''
    Delete an API Management API.
    '''
    return call_az("az apim api delete", locals())


def update(api_id, resource_group, service_name, add=None, api_type=None, description=None, display_name=None, force_string=None, if_match=None, no_wait=None, path=None, protocols=None, remove=None, service_url=None, set=None, subscription_key_header_name=None, subscription_key_query_param_name=None, subscription_required=None, tags=None):
    '''
    Update an API Management API.
    '''
    return call_az("az apim api update", locals())


def wait(api_id, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of an apim api is met.
    '''
    return call_az("az apim api wait", locals())

