from ... pyaz_utils import call_az
from . import address_pool, frontend_ip, probe, rule


def show(name, resource_group, expand=None):
    return call_az("az network cross-region-lb show", locals())


def create(name, resource_group, backend_pool_name=None, frontend_ip_name=None, frontend_ip_zone=None, location=None, no_wait=None, public_ip_address=None, public_ip_address_allocation=None, public_ip_dns_name=None, public_ip_zone=None, tags=None, validate=None):
    '''
    Create a cross-region load balancer.
    '''
    return call_az("az network cross-region-lb create", locals())


def delete(name, resource_group):
    return call_az("az network cross-region-lb delete", locals())


def list(resource_group=None):
    '''
    List load balancers.
    '''
    return call_az("az network cross-region-lb list", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a cross-region load balancer.
    '''
    return call_az("az network cross-region-lb update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the cross-region load balancer is met.
    '''
    return call_az("az network cross-region-lb wait", locals())

