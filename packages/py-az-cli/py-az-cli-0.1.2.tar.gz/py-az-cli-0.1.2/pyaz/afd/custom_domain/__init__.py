from ... pyaz_utils import call_az

def show(custom_domain_name, profile_name, resource_group):
    '''
    Show the custom domain details.
    '''
    return call_az("az afd custom-domain show", locals())


def wait(custom_domain_name, profile_name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the custom domain is met.
    '''
    return call_az("az afd custom-domain wait", locals())


def delete(custom_domain_name, profile_name, resource_group, yes=None):
    '''
    Delete a custom domain.
    '''
    return call_az("az afd custom-domain delete", locals())


def list(profile_name, resource_group):
    '''
    List all the custom domains within the specified profile.
    '''
    return call_az("az afd custom-domain list", locals())


def create(certificate_type, custom_domain_name, host_name, minimum_tls_version, profile_name, resource_group, azure_dns_zone=None, no_wait=None, secret=None):
    '''
    Create a custom domain within the specified profile.
    '''
    return call_az("az afd custom-domain create", locals())


def update(custom_domain_name, profile_name, resource_group, azure_dns_zone=None, certificate_type=None, minimum_tls_version=None, secret=None):
    '''
    Update a custom domain within the specified profile.
    '''
    return call_az("az afd custom-domain update", locals())

