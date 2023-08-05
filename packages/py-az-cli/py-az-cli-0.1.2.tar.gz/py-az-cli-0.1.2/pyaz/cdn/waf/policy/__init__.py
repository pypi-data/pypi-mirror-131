from .... pyaz_utils import call_az
from . import custom_rule, managed_rule_set, rate_limit_rule


def show(name, resource_group):
    '''
    Show details of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy show", locals())


def list(resource_group):
    '''
    List CDN WAF policies.
    '''
    return call_az("az cdn waf policy list", locals())


def set(name, resource_group, block_response_body=None, block_response_status_code=None, disabled=None, mode=None, redirect_url=None, sku=None, tags=None):
    '''
    Create a new CDN WAF policy.
    '''
    return call_az("az cdn waf policy set", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a CDN WAF policy.
    '''
    return call_az("az cdn waf policy delete", locals())

