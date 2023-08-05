from .... pyaz_utils import call_az
from . import ipsec_policy


def generate(name, resource_group, authentication_method=None, client_root_certificates=None, processor_architecture=None, radius_server_auth_certificate=None, use_legacy=None):
    '''
    Generate VPN client configuration.
    '''
    return call_az("az network vnet-gateway vpn-client generate", locals())


def show_url(name, resource_group):
    '''
    Retrieve a pre-generated VPN client configuration.
    '''
    return call_az("az network vnet-gateway vpn-client show-url", locals())


def show_health(name, resource_group):
    '''
    Get the VPN client connection health detail per P2S client connection of the virtual network gateway.
    '''
    return call_az("az network vnet-gateway vpn-client show-health", locals())

