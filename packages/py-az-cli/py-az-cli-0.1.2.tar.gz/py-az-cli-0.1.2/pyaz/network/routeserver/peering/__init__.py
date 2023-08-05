from .... pyaz_utils import call_az

def create(name, peer_asn, peer_ip, resource_group, routeserver, no_wait=None):
    '''
    Create a route server peering.
    '''
    return call_az("az network routeserver peering create", locals())


def update(name, resource_group, routeserver, add=None, force_string=None, peer_asn=None, peer_ip=None, remove=None, set=None):
    '''
    Update a route server peering.
    '''
    return call_az("az network routeserver peering update", locals())


def delete(name, resource_group, routeserver, no_wait=None, yes=None):
    '''
    Delete a route server peering.
    '''
    return call_az("az network routeserver peering delete", locals())


def show(name, resource_group, routeserver):
    '''
    Show a route server peering
    '''
    return call_az("az network routeserver peering show", locals())


def wait(name, resource_group, routeserver, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the route server peering is met.
    '''
    return call_az("az network routeserver peering wait", locals())


def list(resource_group, routeserver):
    '''
    List all route server peerings under a resource group.
    '''
    return call_az("az network routeserver peering list", locals())


def list_learned_routes(name, resource_group, routeserver):
    '''
    List all routes the route server bgp connection has learned.
    '''
    return call_az("az network routeserver peering list-learned-routes", locals())


def list_advertised_routes(name, resource_group, routeserver):
    '''
    List all routes the route server bgp connection is advertising to the specified peer.
    '''
    return call_az("az network routeserver peering list-advertised-routes", locals())

