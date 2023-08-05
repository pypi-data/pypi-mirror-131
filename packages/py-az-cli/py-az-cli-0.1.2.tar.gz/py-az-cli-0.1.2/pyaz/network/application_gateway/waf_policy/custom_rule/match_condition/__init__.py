from ...... pyaz_utils import call_az

def add(match_variables, name, operator, policy_name, resource_group, values, negate=None, transforms=None):
    '''
    A match condition to an application gateway WAF policy custom rule.
    '''
    return call_az("az network application-gateway waf-policy custom-rule match-condition add", locals())


def list(name, policy_name, resource_group):
    '''
    List application gateway WAF policy custom rule match conditions.
    '''
    return call_az("az network application-gateway waf-policy custom-rule match-condition list", locals())


def remove(index, name, policy_name, resource_group):
    '''
    Remove a match condition from an application gateway WAF policy custom rule.
    '''
    return call_az("az network application-gateway waf-policy custom-rule match-condition remove", locals())

