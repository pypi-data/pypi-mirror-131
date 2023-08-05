from ..... pyaz_utils import call_az

def create(gateway_name, name, path_map_name, paths, resource_group, address_pool=None, http_settings=None, no_wait=None, redirect_config=None, rewrite_rule_set=None, waf_policy=None):
    '''
    Create a rule for a URL path map.
    '''
    return call_az("az network application-gateway url-path-map rule create", locals())


def delete(gateway_name, name, path_map_name, resource_group, no_wait=None):
    '''
    Delete a rule of a URL path map.
    '''
    return call_az("az network application-gateway url-path-map rule delete", locals())

