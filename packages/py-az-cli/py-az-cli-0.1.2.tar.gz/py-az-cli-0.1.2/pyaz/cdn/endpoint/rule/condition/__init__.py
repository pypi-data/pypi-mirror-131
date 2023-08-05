from ..... pyaz_utils import call_az

def show(name, profile_name, resource_group):
    '''
    show delivery rules asscociate with the endpoint.
    '''
    return call_az("az cdn endpoint rule condition show", locals())


def add(match_variable, name, operator, profile_name, resource_group, rule_name, match_values=None, negate_condition=None, selector=None, transform=None):
    '''
    Add a condition to a delivery rule.
    '''
    return call_az("az cdn endpoint rule condition add", locals())


def remove(index, name, profile_name, resource_group, rule_name):
    '''
    Remove a condition from a delivery rule.
    '''
    return call_az("az cdn endpoint rule condition remove", locals())

