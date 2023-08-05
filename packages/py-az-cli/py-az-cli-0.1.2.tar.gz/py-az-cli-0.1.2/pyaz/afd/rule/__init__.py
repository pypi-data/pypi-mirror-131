from ... pyaz_utils import call_az
from . import action, condition


def show(profile_name, resource_group, rule_name, rule_set_name):
    '''
    Show delivery rule details.
    '''
    return call_az("az afd rule show", locals())


def list(profile_name, resource_group, rule_set_name):
    return call_az("az afd rule list", locals())


def create(action_name, order, profile_name, resource_group, rule_name, rule_set_name, cache_behavior=None, cache_duration=None, custom_fragment=None, custom_hostname=None, custom_path=None, custom_querystring=None, destination=None, header_action=None, header_name=None, header_value=None, match_processing_behavior=None, match_values=None, match_variable=None, negate_condition=None, operator=None, preserve_unmatched_path=None, query_parameters=None, query_string_behavior=None, redirect_protocol=None, redirect_type=None, selector=None, source_pattern=None, transform=None):
    '''
    Creates a new delivery rule within the specified rule set.
    '''
    return call_az("az afd rule create", locals())


def delete(profile_name, resource_group, rule_name, rule_set_name, yes=None):
    '''
    Remove a delivery rule from rule set.
    '''
    return call_az("az afd rule delete", locals())

