from ...... pyaz_utils import call_az

def add(policy_name, resource_group, type, version, group_name=None, rules=None):
    '''
    Add managed rule set to the WAF policy managed rules. For rule set and rules, please visit: https://docs.microsoft.com/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules

    '''
    return call_az("az network application-gateway waf-policy managed-rule rule-set add", locals())


def update(policy_name, resource_group, type, version, add=None, force_string=None, group_name=None, remove=None, rules=None, set=None):
    '''
    Manage rules of a WAF policy. If --group-name and --rules are provided, override existing rules. If --group-name is provided, clear all rules under a certain rule group. If neither of them are provided, update rule set and clear all rules under itself. For rule set and rules, please visit: https://docs.microsoft.com/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules

    '''
    return call_az("az network application-gateway waf-policy managed-rule rule-set update", locals())


def remove(policy_name, resource_group, type, version, group_name=None):
    '''
    Remove a managed rule set by rule set group name if rule_group_name is specified. Otherwise, remove all rule set.

    '''
    return call_az("az network application-gateway waf-policy managed-rule rule-set remove", locals())


def list(policy_name, resource_group):
    '''
    List all managed rule set.
    '''
    return call_az("az network application-gateway waf-policy managed-rule rule-set list", locals())

