from ....... pyaz_utils import call_az

def add(match_variable, policy_name, resource_group, selector, selector_match_operator, type, version, group_name=None, rule_ids=None):
    '''
    Add a managed rule set to an exclusion.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion rule-set add", locals())


def remove(match_variable, policy_name, resource_group, selector, selector_match_operator, type, version, group_name=None):
    '''
    Remove managed rule set within an exclusion.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion rule-set remove", locals())


def list(policy_name, resource_group):
    '''
    List all managed rule sets of an exclusion.
    '''
    return call_az("az network application-gateway waf-policy managed-rule exclusion rule-set list", locals())

