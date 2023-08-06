from ... pyaz_utils import _call_az

def show(profile_name, resource_group, security_policy_name):
    return _call_az("az afd security-policy show", locals())


def list(profile_name, resource_group):
    return _call_az("az afd security-policy list", locals())


def create(domains, profile_name, resource_group, security_policy_name, waf_policy):
    '''
    Creates a new security policy within the specified profile.
    '''
    return _call_az("az afd security-policy create", locals())


def update(profile_name, resource_group, security_policy_name, domains=None, waf_policy=None):
    '''
    Update an existing security policy within the specified profile.
    '''
    return _call_az("az afd security-policy update", locals())


def delete(profile_name, resource_group, security_policy_name, yes=None):
    return _call_az("az afd security-policy delete", locals())

