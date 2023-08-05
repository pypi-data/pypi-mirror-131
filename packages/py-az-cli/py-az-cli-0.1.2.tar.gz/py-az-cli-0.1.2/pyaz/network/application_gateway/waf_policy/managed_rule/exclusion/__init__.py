from ...... pyaz_utils import call_az
from . import rule_set


def add(match_variable, policy_name, resource_group, selector, selector_match_operator):
    '''
    Add an OWASP CRS exclusion rule to the WAF policy managed rules.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion add", locals())


def remove(policy_name, resource_group):
    '''
    Remove all OWASP CRS exclusion rules that are applied on a Waf policy managed rules.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion remove", locals())


def list(policy_name, resource_group):
    '''
    List all OWASP CRS exclusion rules that are applied on a Waf policy managed rules.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion list", locals())

