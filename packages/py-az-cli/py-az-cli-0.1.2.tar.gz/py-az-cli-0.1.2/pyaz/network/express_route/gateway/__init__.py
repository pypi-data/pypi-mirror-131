from .... pyaz_utils import call_az
from . import connection


def create(name, resource_group, location=None, max_val=None, min_val=None, tags=None, virtual_hub=None):
    '''
    Create an ExpressRoute gateway.
    '''
    return call_az("az network express-route gateway create", locals())


def delete(name, resource_group):
    '''
    Delete an ExpressRoute gateway.
    '''
    return call_az("az network express-route gateway delete", locals())


def list(resource_group=None):
    '''
    List ExpressRoute gateways.
    '''
    return call_az("az network express-route gateway list", locals())


def show(name, resource_group):
    '''
    Get the details of an ExpressRoute gateway.
    '''
    return call_az("az network express-route gateway show", locals())


def update(name, resource_group, add=None, force_string=None, max_val=None, min_val=None, remove=None, set=None, tags=None):
    '''
    Update settings of an ExpressRoute gateway.
    '''
    return call_az("az network express-route gateway update", locals())

