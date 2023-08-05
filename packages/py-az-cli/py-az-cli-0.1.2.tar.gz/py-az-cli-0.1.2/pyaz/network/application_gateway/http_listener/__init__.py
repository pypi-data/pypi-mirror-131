from .... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List HTTP listeners.
    '''
    return call_az("az network application-gateway http-listener list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of an HTTP listener.
    '''
    return call_az("az network application-gateway http-listener show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete an HTTP listener.
    '''
    return call_az("az network application-gateway http-listener delete", locals())


def create(frontend_port, gateway_name, name, resource_group, frontend_ip=None, host_name=None, host_names=None, no_wait=None, ssl_cert=None, ssl_profile_id=None, waf_policy=None):
    '''
    Create an HTTP listener.
    '''
    return call_az("az network application-gateway http-listener create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, frontend_ip=None, frontend_port=None, host_name=None, host_names=None, no_wait=None, remove=None, set=None, ssl_cert=None, ssl_profile_id=None, waf_policy=None):
    '''
    Update an HTTP listener.
    '''
    return call_az("az network application-gateway http-listener update", locals())

