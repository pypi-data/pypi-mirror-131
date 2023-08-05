from ... pyaz_utils import call_az
from . import client_certificate


def list(resource_group=None):
    '''
    List managed clusters.
    '''
    return call_az("az sf managed-cluster list", locals())


def delete(cluster_name, resource_group):
    '''
    Delete a managed cluster.
    '''
    return call_az("az sf managed-cluster delete", locals())


def show(cluster_name, resource_group):
    '''
    Show the properties of an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-cluster show", locals())


def create(admin_password, cluster_name, resource_group, admin_user_name=None, client_cert_common_name=None, client_cert_is_admin=None, client_cert_issuer_thumbprint=None, client_cert_thumbprint=None, client_connection_port=None, cluster_code_version=None, cluster_upgrade_cadence=None, cluster_upgrade_mode=None, dns_name=None, gateway_connection_port=None, location=None, sku=None, tags=None):
    '''
    Delete a managed cluster.
    '''
    return call_az("az sf managed-cluster create", locals())


def update(cluster_name, resource_group, client_connection_port=None, dns_name=None, gateway_connection_port=None, tags=None):
    '''
    Update a managed cluster.
    '''
    return call_az("az sf managed-cluster update", locals())

