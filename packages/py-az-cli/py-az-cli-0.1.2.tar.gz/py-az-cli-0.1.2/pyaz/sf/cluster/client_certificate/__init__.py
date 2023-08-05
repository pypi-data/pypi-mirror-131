from .... pyaz_utils import call_az

def add(cluster_name, resource_group, admin_client_thumbprints=None, certificate_common_name=None, certificate_issuer_thumbprint=None, client_certificate_common_names=None, is_admin=None, readonly_client_thumbprints=None, thumbprint=None):
    '''
    Add a common name or certificate thumbprint to the cluster for client authentication.
    '''
    return call_az("az sf cluster client-certificate add", locals())


def remove(cluster_name, resource_group, certificate_common_name=None, certificate_issuer_thumbprint=None, client_certificate_common_names=None, thumbprints=None):
    '''
    Remove client certificates or subject names used for authentication.
    '''
    return call_az("az sf cluster client-certificate remove", locals())

