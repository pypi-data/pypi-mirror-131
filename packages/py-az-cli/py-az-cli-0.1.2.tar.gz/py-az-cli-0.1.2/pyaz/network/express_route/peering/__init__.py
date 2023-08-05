from .... pyaz_utils import call_az
from . import connection, peer_connection


def create(circuit_name, peer_asn, peering_type, primary_peer_subnet, resource_group, secondary_peer_subnet, vlan_id, advertised_public_prefixes=None, customer_asn=None, ip_version=None, legacy_mode=None, route_filter=None, routing_registry_name=None, shared_key=None):
    '''
    Create peering settings for an ExpressRoute circuit.
    '''
    return call_az("az network express-route peering create", locals())


def delete(circuit_name, name, resource_group):
    '''
    Delete peering settings.
    '''
    return call_az("az network express-route peering delete", locals())


def show(circuit_name, name, resource_group):
    '''
    Get the details of an express route peering.
    '''
    return call_az("az network express-route peering show", locals())


def list(circuit_name, resource_group):
    '''
    List peering settings of an ExpressRoute circuit.
    '''
    return call_az("az network express-route peering list", locals())


def get_stats(circuit_name, name, resource_group):
    '''
    Get all traffic stats of an ExpressRoute peering.
    '''
    return call_az("az network express-route peering get-stats", locals())


def update(circuit_name, name, resource_group, add=None, advertised_public_prefixes=None, customer_asn=None, force_string=None, ip_version=None, legacy_mode=None, peer_asn=None, primary_peer_subnet=None, remove=None, route_filter=None, routing_registry_name=None, secondary_peer_subnet=None, set=None, shared_key=None, vlan_id=None):
    '''
    Update peering settings of an ExpressRoute circuit.
    '''
    return call_az("az network express-route peering update", locals())

