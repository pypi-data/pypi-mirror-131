from .... pyaz_utils import call_az
from . import ip_config


def add(frontend_ip, gateway_name, name, resource_group, subnet, ip_address=None, no_wait=None, primary=None, subnet_prefix=None):
    '''
    Add a new Private Link with a default IP Configuration and associate it with an existing Frontend IP
    '''
    return call_az("az network application-gateway private-link add", locals())


def remove(gateway_name, name, resource_group, no_wait=None, yes=None):
    '''
    Remove a Private Link and clear association with Frontend IP. The subnet associate with a Private Link might need to clear manually
    '''
    return call_az("az network application-gateway private-link remove", locals())


def show(gateway_name, name, resource_group):
    '''
    Show a Private Link
    '''
    return call_az("az network application-gateway private-link show", locals())


def list(gateway_name, resource_group):
    '''
    List all the Private Link
    '''
    return call_az("az network application-gateway private-link list", locals())


def wait(gateway_name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until the condition of corresponding application gateway is met
    '''
    return call_az("az network application-gateway private-link wait", locals())

