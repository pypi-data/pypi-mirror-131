from ..... pyaz_utils import call_az

def set(action, duration, name, policy_name, priority, request_threshold, resource_group, disabled=None):
    '''
    Add a rate limit rule to a CDN WAF policy.
    '''
    return call_az("az cdn waf policy rate-limit-rule set", locals())


def delete(name, policy_name, resource_group, yes=None):
    '''
    Remove a rate limit rule from a CDN WAF policy.
    '''
    return call_az("az cdn waf policy rate-limit-rule delete", locals())


def list(policy_name, resource_group):
    '''
    List rate limit rules of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy rate-limit-rule list", locals())


def show(name, policy_name, resource_group):
    '''
    Show a rate limit rule of a CDN WAF policy.
    '''
    return call_az("az cdn waf policy rate-limit-rule show", locals())

