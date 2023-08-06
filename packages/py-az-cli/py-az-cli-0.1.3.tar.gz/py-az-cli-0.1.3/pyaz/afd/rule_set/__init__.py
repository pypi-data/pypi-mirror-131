from ... pyaz_utils import _call_az

def show(profile_name, resource_group, rule_set_name):
    return _call_az("az afd rule-set show", locals())


def list(profile_name, resource_group):
    return _call_az("az afd rule-set list", locals())


def create(profile_name, resource_group, rule_set_name):
    '''
    Creates a new rule set under the specified profile.
    '''
    return _call_az("az afd rule-set create", locals())


def delete(profile_name, resource_group, rule_set_name, yes=None):
    '''
    Delete the rule set.
    '''
    return _call_az("az afd rule-set delete", locals())

