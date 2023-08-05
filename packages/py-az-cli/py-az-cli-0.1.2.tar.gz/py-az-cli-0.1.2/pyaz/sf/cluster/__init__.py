from ... pyaz_utils import call_az
from . import client_certificate, durability, node, node_type, reliability, setting, upgrade_type


def show(cluster_name, resource_group):
    return call_az("az sf cluster show", locals())


def list(resource_group=None):
    '''
    List cluster resources.
    '''
    return call_az("az sf cluster list", locals())


def create(resource_group, certificate_file=None, certificate_output_folder=None, certificate_password=None, certificate_subject_name=None, cluster_name=None, cluster_size=None, location=None, parameter_file=None, secret_identifier=None, template_file=None, vault_name=None, vault_rg=None, vm_os=None, vm_password=None, vm_sku=None, vm_user_name=None):
    '''
    Create a new Azure Service Fabric cluster.
    '''
    return call_az("az sf cluster create", locals())

