from .... pyaz_utils import call_az

def create(name, resource_group, idle_timeout=None, location=None, no_wait=None, public_ip_addresses=None, public_ip_prefixes=None, zone=None):
    '''
    Create a NAT gateway.
    '''
    return call_az("az network nat gateway create", locals())


def delete(name, resource_group):
    '''
    Delete a NAT gateway.
    '''
    return call_az("az network nat gateway delete", locals())


def list(resource_group=None):
    '''
    List NAT gateways.
    '''
    return call_az("az network nat gateway list", locals())


def show(name, resource_group):
    '''
    Show details of a NAT gateway.
    '''
    return call_az("az network nat gateway show", locals())


def update(name, resource_group, add=None, force_string=None, idle_timeout=None, public_ip_addresses=None, public_ip_prefixes=None, remove=None, set=None):
    '''
    Update a NAT gateway.
    '''
    return call_az("az network nat gateway update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the NAT gateway is met.
    '''
    return call_az("az network nat gateway wait", locals())

