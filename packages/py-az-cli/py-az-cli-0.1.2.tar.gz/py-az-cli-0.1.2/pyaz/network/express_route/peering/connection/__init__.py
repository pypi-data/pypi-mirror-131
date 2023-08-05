from ..... pyaz_utils import call_az
from . import ipv6_config


def create(address_prefix, circuit_name, name, peer_circuit, peering_name, resource_group, authorization_key=None):
    '''
    Create connections between two ExpressRoute circuits.
    '''
    return call_az("az network express-route peering connection create", locals())


def delete(circuit_name, name, peering_name, resource_group):
    '''
    Delete an ExpressRoute circuit connection.
    '''
    return call_az("az network express-route peering connection delete", locals())


def show(circuit_name, name, peering_name, resource_group):
    '''
    Get the details of an ExpressRoute circuit connection.
    '''
    return call_az("az network express-route peering connection show", locals())


def list(circuit_name, peering_name, resource_group):
    '''
    List all global reach connections associated with a private peering in an express route circuit.
    '''
    return call_az("az network express-route peering connection list", locals())

