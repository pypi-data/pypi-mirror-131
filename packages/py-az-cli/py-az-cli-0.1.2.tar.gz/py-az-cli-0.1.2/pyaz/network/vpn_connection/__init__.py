from ... pyaz_utils import call_az
from . import ipsec_policy, packet_capture, shared_key


def create(name, resource_group, vnet_gateway1, authorization_key=None, egress_nat_rule=None, enable_bgp=None, express_route_circuit2=None, express_route_gateway_bypass=None, ingress_nat_rule=None, local_gateway2=None, location=None, routing_weight=None, shared_key=None, tags=None, use_policy_based_traffic_selectors=None, validate=None, vnet_gateway2=None):
    '''
    Create a VPN connection.
    '''
    return call_az("az network vpn-connection create", locals())


def delete(name, resource_group):
    '''
    Delete a VPN connection.
    '''
    return call_az("az network vpn-connection delete", locals())


def show(name, resource_group):
    '''
    Get the details of a VPN connection.
    '''
    return call_az("az network vpn-connection show", locals())


def list(resource_group, vnet_gateway=None):
    '''
    List all VPN connections.
    '''
    return call_az("az network vpn-connection list", locals())


def update(name, resource_group, add=None, enable_bgp=None, express_route_gateway_bypass=None, force_string=None, remove=None, routing_weight=None, set=None, shared_key=None, tags=None, use_policy_based_traffic_selectors=None):
    '''
    Update a VPN connection.
    '''
    return call_az("az network vpn-connection update", locals())


def list_ike_sas(name, resource_group):
    '''
    List IKE Security Associations for a VPN connection.
    '''
    return call_az("az network vpn-connection list-ike-sas", locals())


def show_device_config_script(device_family, firmware_version, name, resource_group, vendor):
    '''
    Get a XML format representation for VPN connection device configuration script.
    '''
    return call_az("az network vpn-connection show-device-config-script", locals())

