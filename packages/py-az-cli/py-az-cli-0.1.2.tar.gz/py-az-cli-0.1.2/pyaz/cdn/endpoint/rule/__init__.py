from .... pyaz_utils import call_az
from . import action, condition


def show(name, profile_name, resource_group):
    '''
    Show delivery rules asscociate with the endpoint.
    '''
    return call_az("az cdn endpoint rule show", locals())


def add(action_name, name, order, profile_name, resource_group, cache_behavior=None, cache_duration=None, custom_fragment=None, custom_hostname=None, custom_path=None, custom_querystring=None, destination=None, header_action=None, header_name=None, header_value=None, match_values=None, match_variable=None, negate_condition=None, operator=None, origin_group=None, preserve_unmatched_path=None, query_parameters=None, query_string_behavior=None, redirect_protocol=None, redirect_type=None, rule_name=None, selector=None, source_pattern=None, transform=None):
    '''
    Add a delivery rule to a CDN endpoint.
    '''
    return call_az("az cdn endpoint rule add", locals())


def remove(name, profile_name, resource_group, order=None, rule_name=None):
    '''
    Remove a delivery rule from an endpoint.
    '''
    return call_az("az cdn endpoint rule remove", locals())

