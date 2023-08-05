from ..... pyaz_utils import call_az

def add(gateway_name, name, private_link, resource_group, ip_address=None, no_wait=None, primary=None):
    '''
    Add an IP configuration to a Private Link to scale up its capability
    '''
    return call_az("az network application-gateway private-link ip-config add", locals())


def remove(gateway_name, name, private_link, resource_group, no_wait=None, yes=None):
    '''
    Remove an IP configuration from a Private Link to scale down its capability
    '''
    return call_az("az network application-gateway private-link ip-config remove", locals())


def show(gateway_name, name, private_link, resource_group):
    '''
    Show an IP configuration of a Private Link
    '''
    return call_az("az network application-gateway private-link ip-config show", locals())


def list(gateway_name, private_link, resource_group):
    '''
    List all the IP configuration of a Private Link
    '''
    return call_az("az network application-gateway private-link ip-config list", locals())


def wait(gateway_name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until the condition of corresponding application gateway is met
    '''
    return call_az("az network application-gateway private-link ip-config wait", locals())

