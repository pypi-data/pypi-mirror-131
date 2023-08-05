from ..... pyaz_utils import call_az

def show(endpoint_name, profile_name, resource_group):
    '''
    Show which CDN WAF policy is applied to a CDN endpoint.
    '''
    return call_az("az cdn endpoint waf policy show", locals())


def set(endpoint_name, profile_name, resource_group, waf_policy_id=None, waf_policy_name=None, waf_policy_resource_group_name=None, waf_policy_subscription_id=None):
    '''
    Set the CDN WAF policy applied to a CDN endpoint
    '''
    return call_az("az cdn endpoint waf policy set", locals())


def remove(endpoint_name, profile_name, resource_group, yes=None):
    '''
    Remove a CDN WAF policy from a CDN endpoint.
    '''
    return call_az("az cdn endpoint waf policy remove", locals())

