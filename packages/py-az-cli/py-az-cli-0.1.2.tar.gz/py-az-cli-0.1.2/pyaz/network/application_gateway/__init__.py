from ... pyaz_utils import call_az
from . import address_pool, auth_cert, client_cert, frontend_ip, frontend_port, http_listener, http_settings, identity, private_link, probe, redirect_config, root_cert, rule, ssl_cert, ssl_policy, ssl_profile, url_path_map, waf_config, waf_policy


def create(name, resource_group, capacity=None, cert_file=None, cert_password=None, connection_draining_timeout=None, custom_error_pages=None, enable_private_link=None, frontend_port=None, http2=None, http_settings_cookie_based_affinity=None, http_settings_port=None, http_settings_protocol=None, identity=None, key_vault_secret_id=None, location=None, max_capacity=None, min_capacity=None, no_wait=None, private_ip_address=None, private_link_ip_address=None, private_link_primary=None, private_link_subnet=None, private_link_subnet_prefix=None, public_ip_address=None, public_ip_address_allocation=None, routing_rule_type=None, servers=None, sku=None, ssl_certificate_name=None, ssl_profile=None, ssl_profile_id=None, subnet=None, subnet_address_prefix=None, tags=None, trusted_client_cert=None, validate=None, vnet_address_prefix=None, vnet_name=None, waf_policy=None, zones=None):
    '''
    Create an application gateway.
    '''
    return call_az("az network application-gateway create", locals())


def delete(name, resource_group, no_wait=None):
    '''
    Delete an application gateway.
    '''
    return call_az("az network application-gateway delete", locals())


def show(name, resource_group):
    '''
    Get the details of an application gateway.
    '''
    return call_az("az network application-gateway show", locals())


def list(resource_group=None):
    '''
    List application gateways.
    '''
    return call_az("az network application-gateway list", locals())


def start(name, resource_group):
    '''
    Start an application gateway.
    '''
    return call_az("az network application-gateway start", locals())


def stop(name, resource_group):
    '''
    Stop an application gateway.
    '''
    return call_az("az network application-gateway stop", locals())


def show_backend_health(name, resource_group, address_pool=None, expand=None, host=None, host_name_from_http_settings=None, http_settings=None, match_body=None, match_status_codes=None, path=None, protocol=None, timeout=None):
    '''
    Get information on the backend health of an application gateway.
    '''
    return call_az("az network application-gateway show-backend-health", locals())


def update(name, resource_group, add=None, capacity=None, custom_error_pages=None, force_string=None, http2=None, max_capacity=None, min_capacity=None, no_wait=None, remove=None, set=None, sku=None, tags=None):
    '''
    Update an application gateway.
    '''
    return call_az("az network application-gateway update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the application gateway is met.
    '''
    return call_az("az network application-gateway wait", locals())

