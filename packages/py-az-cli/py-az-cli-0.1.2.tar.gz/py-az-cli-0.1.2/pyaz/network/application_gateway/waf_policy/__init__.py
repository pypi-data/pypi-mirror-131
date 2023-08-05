from .... pyaz_utils import call_az
from . import custom_rule, policy_setting


def create(name, resource_group, location=None, tags=None, type=None, version=None):
    '''
    Create an application gateway WAF policy.
    '''
    return call_az("az network application-gateway waf-policy create", locals())


def delete(name, resource_group):
    '''
    Delete an application gateway WAF policy.
    '''
    return call_az("az network application-gateway waf-policy delete", locals())


def show(name, resource_group):
    '''
    Get the details of an application gateway WAF policy.
    '''
    return call_az("az network application-gateway waf-policy show", locals())


def list(resource_group=None):
    '''
    List application gateway WAF policies.
    '''
    return call_az("az network application-gateway waf-policy list", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update an application gateway WAF policy.
    '''
    return call_az("az network application-gateway waf-policy update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the application gateway WAF policy is met.
    '''
    return call_az("az network application-gateway waf-policy wait", locals())

