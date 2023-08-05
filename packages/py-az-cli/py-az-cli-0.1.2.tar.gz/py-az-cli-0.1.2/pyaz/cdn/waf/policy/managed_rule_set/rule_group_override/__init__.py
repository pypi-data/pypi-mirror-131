from ...... pyaz_utils import call_az

def set(name, policy_name, resource_group, rule_set_type, rule_set_version):
    '''
    Add or update a rule group override to a managed rule set on a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set rule-group-override set", locals())


def delete(name, policy_name, resource_group, rule_set_type, rule_set_version, yes=None):
    '''
    Remove a rule group override from a managed rule set on a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set rule-group-override delete", locals())


def list(policy_name, resource_group, rule_set_type, rule_set_version):
    '''
    List rule group overrides of a managed rule on a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set rule-group-override list", locals())


def show(name, policy_name, resource_group, rule_set_type, rule_set_version):
    '''
    Show a rule group override of a managed rule on a CDN WAF policy.
    '''
    return call_az("az cdn waf policy managed-rule-set rule-group-override show", locals())


def list_available(rule_set_type, rule_set_version):
    '''
    List available CDN WAF managed rule groups of a managed rule set.
    '''
    return call_az("az cdn waf policy managed-rule-set rule-group-override list-available", locals())

