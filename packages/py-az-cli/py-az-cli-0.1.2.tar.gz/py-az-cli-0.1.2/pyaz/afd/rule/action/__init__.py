from .... pyaz_utils import call_az

def add(action_name, profile_name, resource_group, rule_name, rule_set_name, cache_behavior=None, cache_duration=None, custom_fragment=None, custom_hostname=None, custom_path=None, custom_querystring=None, destination=None, header_action=None, header_name=None, header_value=None, preserve_unmatched_path=None, query_parameters=None, query_string_behavior=None, redirect_protocol=None, redirect_type=None, source_pattern=None):
    '''
    Add an action to a delivery rule.
    '''
    return call_az("az afd rule action add", locals())


def remove(index, profile_name, resource_group, rule_name, rule_set_name):
    '''
    Remove an action from a delivery rule.
    '''
    return call_az("az afd rule action remove", locals())


def list(profile_name, resource_group, rule_name, rule_set_name):
    '''
    show actions asscociated with the rule.
    '''
    return call_az("az afd rule action list", locals())

