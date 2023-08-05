from ..... pyaz_utils import call_az

def show(name, profile_name, resource_group):
    '''
    show delivery rules asscociate with the endpoint.
    '''
    return call_az("az cdn endpoint rule action show", locals())


def add(action_name, name, profile_name, resource_group, rule_name, cache_behavior=None, cache_duration=None, custom_fragment=None, custom_hostname=None, custom_path=None, custom_querystring=None, destination=None, header_action=None, header_name=None, header_value=None, origin_group=None, preserve_unmatched_path=None, query_parameters=None, query_string_behavior=None, redirect_protocol=None, redirect_type=None, source_pattern=None):
    '''
    Add an action to a delivery rule.
    '''
    return call_az("az cdn endpoint rule action add", locals())


def remove(index, name, profile_name, resource_group, rule_name):
    '''
    Remove an action from a delivery rule.
    '''
    return call_az("az cdn endpoint rule action remove", locals())

