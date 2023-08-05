from ... pyaz_utils import call_az

def show(endpoint_name, profile_name, resource_group, route_name):
    '''
    Show route details.
    '''
    return call_az("az afd route show", locals())


def list(endpoint_name, profile_name, resource_group):
    '''
    List all the routes within the specified endpoint.
    '''
    return call_az("az afd route list", locals())


def create(endpoint_name, forwarding_protocol, https_redirect, origin_group, profile_name, resource_group, route_name, supported_protocols, content_types_to_compress=None, custom_domains=None, enable_compression=None, link_to_default_domain=None, origin_path=None, patterns_to_match=None, query_string_caching_behavior=None, rule_sets=None):
    '''
    Creates a new route within the specified endpoint.
    '''
    return call_az("az afd route create", locals())


def update(endpoint_name, profile_name, resource_group, route_name, content_types_to_compress=None, custom_domains=None, enable_compression=None, forwarding_protocol=None, https_redirect=None, link_to_default_domain=None, origin_group=None, origin_path=None, patterns_to_match=None, query_string_caching_behavior=None, rule_sets=None, supported_protocols=None):
    '''
    Update an existing route within the specified endpoint.
    '''
    return call_az("az afd route update", locals())


def delete(endpoint_name, profile_name, resource_group, route_name, yes=None):
    '''
    Delete an existing route within the specified endpoint.
    '''
    return call_az("az afd route delete", locals())

