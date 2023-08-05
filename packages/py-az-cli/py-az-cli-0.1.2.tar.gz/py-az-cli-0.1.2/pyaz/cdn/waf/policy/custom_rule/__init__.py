from ..... pyaz_utils import call_az

def set(action, name, policy_name, priority, resource_group, disabled=None):
    '''
    Add a custom rule to a CDN WAF policy.
    '''
    return call_az("az cdn waf policy custom-rule set", locals())


def delete(name, policy_name, resource_group, yes=None):
    '''
    Remove a custom rule from a CDN WAF policy.
    '''
    return call_az("az cdn waf policy custom-rule delete", locals())


def list(policy_name, resource_group):
    '''
    List custom rules of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy custom-rule list", locals())


def show(name, policy_name, resource_group):
    '''
    Show a custom rule of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy custom-rule show", locals())

