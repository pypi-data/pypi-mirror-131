from ... pyaz_utils import call_az
from . import aad, ipsec_policy, nat_rule, packet_capture, revoked_cert, root_cert, vpn_client


def create(name, public_ip_addresses, resource_group, vnet, aad_audience=None, aad_issuer=None, aad_tenant=None, address_prefixes=None, asn=None, bgp_peering_address=None, client_protocol=None, custom_routes=None, edge_zone=None, gateway_default_site=None, gateway_type=None, location=None, nat_rule=None, no_wait=None, peer_weight=None, radius_secret=None, radius_server=None, root_cert_data=None, root_cert_name=None, sku=None, tags=None, vpn_auth_type=None, vpn_gateway_generation=None, vpn_type=None):
    '''
    Create a virtual network gateway.
    '''
    return call_az("az network vnet-gateway create", locals())


def update(name, resource_group, aad_audience=None, aad_issuer=None, aad_tenant=None, add=None, address_prefixes=None, asn=None, bgp_peering_address=None, client_protocol=None, custom_routes=None, enable_bgp=None, force_string=None, gateway_default_site=None, gateway_type=None, no_wait=None, peer_weight=None, public_ip_addresses=None, radius_secret=None, radius_server=None, remove=None, root_cert_data=None, root_cert_name=None, set=None, sku=None, tags=None, vnet=None, vpn_auth_type=None, vpn_type=None):
    '''
    Update a virtual network gateway.
    '''
    return call_az("az network vnet-gateway update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the virtual network gateway is met.
    '''
    return call_az("az network vnet-gateway wait", locals())


def delete(name, resource_group, no_wait=None):
    '''
    Delete a virtual network gateway.
    '''
    return call_az("az network vnet-gateway delete", locals())


def show(name, resource_group):
    '''
    Get the details of a virtual network gateway.
    '''
    return call_az("az network vnet-gateway show", locals())


def list(resource_group):
    '''
    List virtual network gateways.
    '''
    return call_az("az network vnet-gateway list", locals())


def reset(name, resource_group, gateway_vip=None):
    '''
    Reset a virtual network gateway.
    '''
    return call_az("az network vnet-gateway reset", locals())


def list_bgp_peer_status(name, resource_group, peer=None):
    '''
    Retrieve the status of BGP peers.
    '''
    return call_az("az network vnet-gateway list-bgp-peer-status", locals())


def list_advertised_routes(name, peer, resource_group):
    '''
    List the routes of a virtual network gateway advertised to the specified peer.
    '''
    return call_az("az network vnet-gateway list-advertised-routes", locals())


def list_learned_routes(name, resource_group):
    '''
    This operation retrieves a list of routes the virtual network gateway has learned, including routes learned from BGP peers.
    '''
    return call_az("az network vnet-gateway list-learned-routes", locals())


def show_supported_devices(name, resource_group):
    '''
    Get a xml format representation for supported vpn devices.
    '''
    return call_az("az network vnet-gateway show-supported-devices", locals())


def disconnect_vpn_connections(name, resource_group, vpn_connections, no_wait=None):
    '''
    Disconnect vpn connections of virtual network gateway.
    '''
    return call_az("az network vnet-gateway disconnect-vpn-connections", locals())

