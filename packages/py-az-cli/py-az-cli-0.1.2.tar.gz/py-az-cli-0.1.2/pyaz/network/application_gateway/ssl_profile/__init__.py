from .... pyaz_utils import call_az

def add(gateway_name, name, resource_group, cipher_suites=None, client_auth_configuration=None, disabled_ssl_protocols=None, min_protocol_version=None, policy_name=None, policy_type=None, trusted_client_certificates=None):
    '''
    Add ssl profiles of the application gateway.
    '''
    return call_az("az network application-gateway ssl-profile add", locals())


def remove(gateway_name, name, resource_group):
    '''
    Remove an existing ssl profiles of the application gateway.
    '''
    return call_az("az network application-gateway ssl-profile remove", locals())


def list(gateway_name, resource_group):
    '''
    List the existing ssl profiles of the application gateway.
    '''
    return call_az("az network application-gateway ssl-profile list", locals())


def show(gateway_name, name, resource_group):
    '''
    Show an existing ssl profiles of the application gateway.
    '''
    return call_az("az network application-gateway ssl-profile show", locals())


def update(gateway_name, name, resource_group, cipher_suites=None, client_auth_configuration=None, disabled_ssl_protocols=None, min_protocol_version=None, policy_name=None, policy_type=None, trusted_client_certificates=None):
    '''
    Update ssl profiles of the application gateway.
    '''
    return call_az("az network application-gateway ssl-profile update", locals())

