from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List HTTP settings.
    '''
    return call_az("az network application-gateway http-settings list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a gateway's HTTP settings.
    '''
    return call_az("az network application-gateway http-settings show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete HTTP settings.
    '''
    return call_az("az network application-gateway http-settings delete", locals())


def create(gateway_name, name, port, resource_group, affinity_cookie_name=None, auth_certs=None, connection_draining_timeout=None, cookie_based_affinity=None, enable_probe=None, host_name=None, host_name_from_backend_pool=None, no_wait=None, path=None, probe=None, protocol=None, root_certs=None, timeout=None):
    '''
    Create HTTP settings.
    '''
    return call_az("az network application-gateway http-settings create", locals())


def update(gateway_name, name, resource_group, add=None, affinity_cookie_name=None, auth_certs=None, connection_draining_timeout=None, cookie_based_affinity=None, enable_probe=None, force_string=None, host_name=None, host_name_from_backend_pool=None, no_wait=None, path=None, port=None, probe=None, protocol=None, remove=None, root_certs=None, set=None, timeout=None):
    '''
    Update HTTP settings.
    '''
    return call_az("az network application-gateway http-settings update", locals())

