from .... pyaz_utils import call_az
from . import rule


def list(gateway_name, resource_group):
    '''
    List URL path maps.
    '''
    return call_az("az network application-gateway url-path-map list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a URL path map.
    '''
    return call_az("az network application-gateway url-path-map show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a URL path map.
    '''
    return call_az("az network application-gateway url-path-map delete", locals())


def create(gateway_name, name, paths, resource_group, address_pool=None, default_address_pool=None, default_http_settings=None, default_redirect_config=None, default_rewrite_rule_set=None, http_settings=None, no_wait=None, redirect_config=None, rewrite_rule_set=None, rule_name=None, waf_policy=None):
    '''
    Create a URL path map.
    '''
    return call_az("az network application-gateway url-path-map create", locals())


def update(gateway_name, name, resource_group, add=None, default_address_pool=None, default_http_settings=None, default_redirect_config=None, default_rewrite_rule_set=None, force_string=None, no_wait=None, remove=None, set=None):
    '''
    Update a URL path map.
    '''
    return call_az("az network application-gateway url-path-map update", locals())

