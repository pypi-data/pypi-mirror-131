from ... pyaz_utils import call_az

def show(endpoint_name, name, profile_name, resource_group):
    '''
    Show details for the custom domain of a CDN.
    '''
    return call_az("az cdn custom-domain show", locals())


def delete(endpoint_name, name, profile_name, resource_group):
    '''
    Delete the custom domain of a CDN.
    '''
    return call_az("az cdn custom-domain delete", locals())


def list(endpoint_name, profile_name, resource_group):
    return call_az("az cdn custom-domain list", locals())


def create(endpoint_name, hostname, name, profile_name, resource_group, location=None, tags=None):
    '''
    Create a new custom domain to provide a hostname for a CDN endpoint.
    '''
    return call_az("az cdn custom-domain create", locals())


def enable_https(endpoint_name, name, profile_name, resource_group, min_tls_version=None, user_cert_group_name=None, user_cert_protocol_type=None, user_cert_secret_name=None, user_cert_secret_version=None, user_cert_subscription_id=None, user_cert_vault_name=None):
    '''
    Enable HTTPS for a custom domain. The resource name of the custom domain could be obtained using "az cdn custom-domain list".
    '''
    return call_az("az cdn custom-domain enable-https", locals())


def disable_https(endpoint_name, name, profile_name, resource_group):
    return call_az("az cdn custom-domain disable-https", locals())

