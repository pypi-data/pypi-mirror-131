from ...... pyaz_utils import call_az

def set(address_prefix, circuit_name, name, peering_name, resource_group):
    '''
    Set connection config to ExpressRoute circuit connection.
    '''
    return call_az("az network express-route peering connection ipv6-config set", locals())


def remove(circuit_name, name, peering_name, resource_group):
    '''
    Remove connection config to ExpressRoute circuit connection.
    '''
    return call_az("az network express-route peering connection ipv6-config remove", locals())

