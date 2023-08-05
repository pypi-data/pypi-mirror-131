from .... pyaz_utils import call_az
from . import condition, set


def create(gateway_name, name, resource_group, rule_set_name, enable_reroute=None, modified_path=None, modified_query_string=None, no_wait=None, request_headers=None, response_headers=None, sequence=None):
    '''
    Create a rewrite rule.
    '''
    return call_az("az network application-gateway rewrite-rule create", locals())


def show(gateway_name, name, resource_group, rule_set_name):
    '''
    Get the details of a rewrite rule.
    '''
    return call_az("az network application-gateway rewrite-rule show", locals())


def list(gateway_name, resource_group, rule_set_name):
    '''
    List rewrite rules.
    '''
    return call_az("az network application-gateway rewrite-rule list", locals())


def delete(gateway_name, name, resource_group, rule_set_name, no_wait=None):
    '''
    Delete a rewrite rule.
    '''
    return call_az("az network application-gateway rewrite-rule delete", locals())


def update(gateway_name, name, resource_group, rule_set_name, add=None, enable_reroute=None, force_string=None, modified_path=None, modified_query_string=None, no_wait=None, remove=None, request_headers=None, response_headers=None, sequence=None, set=None):
    '''
    Update a rewrite rule.
    '''
    return call_az("az network application-gateway rewrite-rule update", locals())


def list_request_headers():
    return call_az("az network application-gateway rewrite-rule list-request-headers", locals())


def list_response_headers():
    return call_az("az network application-gateway rewrite-rule list-response-headers", locals())

