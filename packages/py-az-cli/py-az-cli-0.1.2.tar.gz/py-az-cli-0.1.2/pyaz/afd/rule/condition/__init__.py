from .... pyaz_utils import call_az

def add(match_variable, operator, profile_name, resource_group, rule_name, rule_set_name, match_values=None, negate_condition=None, selector=None, transform=None):
    '''
    Add a condition to a delivery rule.
    '''
    return call_az("az afd rule condition add", locals())


def remove(index, profile_name, resource_group, rule_name, rule_set_name):
    '''
    Remove a condition from a delivery rule.
    '''
    return call_az("az afd rule condition remove", locals())


def list(profile_name, resource_group, rule_name, rule_set_name):
    '''
    show condtions asscociated with the rule.
    '''
    return call_az("az afd rule condition list", locals())

