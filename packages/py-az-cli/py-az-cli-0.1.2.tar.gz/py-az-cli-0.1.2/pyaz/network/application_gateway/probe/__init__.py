from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List probes.
    '''
    return call_az("az network application-gateway probe list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a probe.
    '''
    return call_az("az network application-gateway probe show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a probe.
    '''
    return call_az("az network application-gateway probe delete", locals())


def create(gateway_name, name, path, protocol, resource_group, host=None, host_name_from_http_settings=None, interval=None, match_body=None, match_status_codes=None, min_servers=None, no_wait=None, port=None, threshold=None, timeout=None):
    '''
    Create a probe.
    '''
    return call_az("az network application-gateway probe create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, host=None, host_name_from_http_settings=None, interval=None, match_body=None, match_status_codes=None, min_servers=None, no_wait=None, path=None, port=None, protocol=None, remove=None, set=None, threshold=None, timeout=None):
    '''
    Update a probe.
    '''
    return call_az("az network application-gateway probe update", locals())

