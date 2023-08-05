from .... pyaz_utils import call_az
from . import predefined


def set(gateway_name, resource_group, cipher_suites=None, disabled_ssl_protocols=None, min_protocol_version=None, name=None, no_wait=None, policy_type=None):
    '''
    Update or clear SSL policy settings.
    '''
    return call_az("az network application-gateway ssl-policy set", locals())


def show(gateway_name, resource_group):
    '''
    Get the details of gateway's SSL policy settings.
    '''
    return call_az("az network application-gateway ssl-policy show", locals())


def list_options():
    '''
    Lists available SSL options for configuring SSL policy.
    '''
    return call_az("az network application-gateway ssl-policy list-options", locals())

