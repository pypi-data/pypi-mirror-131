from .... pyaz_utils import call_az
from . import identity, link, location


def create(name, resource_group, bandwidth=None, encapsulation=None, location=None, peering_location=None, tags=None):
    '''
    Create an ExpressRoute port.
    '''
    return call_az("az network express-route port create", locals())


def delete(name, resource_group):
    '''
    Delete an ExpressRoute port.
    '''
    return call_az("az network express-route port delete", locals())


def list(resource_group=None):
    '''
    List ExpressRoute ports.
    '''
    return call_az("az network express-route port list", locals())


def show(name, resource_group):
    '''
    Get the details of an ExpressRoute port.
    '''
    return call_az("az network express-route port show", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update settings of an ExpressRoute port.
    '''
    return call_az("az network express-route port update", locals())


def generate_loa(customer_name, name, resource_group, file=None):
    '''
    Generate and download a letter of authorization for the requested ExpressRoutePort
    '''
    return call_az("az network express-route port generate-loa", locals())

