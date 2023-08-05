from ..... pyaz_utils import call_az
from . import rule_group_override


def add(policy_name, resource_group, rule_set_type, rule_set_version):
    '''
    Add a managed rule set to a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set add", locals())


def remove(policy_name, resource_group, rule_set_type, rule_set_version, yes=None):
    '''
    Remove a managed rule set from a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set remove", locals())


def list(policy_name, resource_group):
    '''
    List managed rule sets added to a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set list", locals())


def show(policy_name, resource_group, rule_set_type, rule_set_version):
    '''
    Show a managed rule of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set show", locals())


def list_available():
    '''
    List available CDN WAF managed rule sets.
    '''
    return call_az("az cdn waf policy managed-rule-set list-available", locals())

