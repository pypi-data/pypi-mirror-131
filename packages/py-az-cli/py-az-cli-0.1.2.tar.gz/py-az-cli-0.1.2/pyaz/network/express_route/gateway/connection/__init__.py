from ..... pyaz_utils import call_az

def create(gateway_name, name, peering, resource_group, associated=None, authorization_key=None, circuit_name=None, internet_security=None, labels=None, propagated=None, routing_weight=None):
    '''
    Create an ExpressRoute gateway connection.
    '''
    return call_az("az network express-route gateway connection create", locals())


def delete(gateway_name, name, resource_group):
    '''
    Delete an ExpressRoute gateway connection.
    '''
    return call_az("az network express-route gateway connection delete", locals())


def list(gateway_name, resource_group):
    '''
    List ExpressRoute gateway connections.
    '''
    return call_az("az network express-route gateway connection list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of an ExpressRoute gateway connection.
    '''
    return call_az("az network express-route gateway connection show", locals())


def update(gateway_name, name, resource_group, add=None, associated=None, authorization_key=None, circuit_name=None, force_string=None, internet_security=None, labels=None, peering=None, propagated=None, remove=None, routing_weight=None, set=None):
    '''
    Update an ExpressRoute gateway connection.
    '''
    return call_az("az network express-route gateway connection update", locals())

