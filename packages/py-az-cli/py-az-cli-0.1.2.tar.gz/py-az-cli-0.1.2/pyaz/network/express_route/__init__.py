from ... pyaz_utils import call_az
from . import auth, gateway, peering, port


def delete(name, resource_group, no_wait=None):
    '''
    Delete an ExpressRoute circuit.
    '''
    return call_az("az network express-route delete", locals())


def show(name, resource_group):
    '''
    Get the details of an ExpressRoute circuit.
    '''
    return call_az("az network express-route show", locals())


def get_stats(name, resource_group):
    '''
    Get the statistics of an ExpressRoute circuit.
    '''
    return call_az("az network express-route get-stats", locals())


def list_arp_tables(name, path, peering_name, resource_group):
    '''
    Show the current Address Resolution Protocol (ARP) table of an ExpressRoute circuit.
    '''
    return call_az("az network express-route list-arp-tables", locals())


def list_route_tables(name, path, peering_name, resource_group):
    '''
    Show the current routing table of an ExpressRoute circuit peering.
    '''
    return call_az("az network express-route list-route-tables", locals())


def list_route_tables_summary(name, path, peering_name, resource_group):
    '''
    Show the current routing table summary of an ExpressRoute circuit peering.
    '''
    return call_az("az network express-route list-route-tables-summary", locals())


def create(bandwidth, name, peering_location, provider, resource_group, allow_classic_operations=None, allow_global_reach=None, express_route_port=None, location=None, no_wait=None, sku_family=None, sku_tier=None, tags=None):
    '''
    Create an ExpressRoute circuit.
    '''
    return call_az("az network express-route create", locals())


def list(resource_group=None):
    '''
    List all ExpressRoute circuits for the current subscription.
    '''
    return call_az("az network express-route list", locals())


def list_service_providers():
    '''
    List available ExpressRoute service providers.
    '''
    return call_az("az network express-route list-service-providers", locals())


def update(name, resource_group, add=None, allow_classic_operations=None, allow_global_reach=None, bandwidth=None, express_route_port=None, force_string=None, no_wait=None, peering_location=None, provider=None, remove=None, set=None, sku_family=None, sku_tier=None, tags=None):
    '''
    Update settings of an ExpressRoute circuit.
    '''
    return call_az("az network express-route update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the ExpressRoute is met.
    '''
    return call_az("az network express-route wait", locals())

