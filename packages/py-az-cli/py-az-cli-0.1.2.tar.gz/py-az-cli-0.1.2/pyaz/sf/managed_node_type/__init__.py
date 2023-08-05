from ... pyaz_utils import call_az
from . import node, vm_extension, vm_secret


def list(cluster_name, resource_group):
    '''
    List node types of a managed cluster.
    '''
    return call_az("az sf managed-node-type list", locals())


def delete(cluster_name, resource_group):
    '''
    Delete node type from a cluster.
    '''
    return call_az("az sf managed-node-type delete", locals())


def show(cluster_name, resource_group):
    '''
    Show the properties of a node type.
    '''
    return call_az("az sf managed-node-type show", locals())


def create(cluster_name, instance_count, resource_group, application_end_port=None, application_start_port=None, capacity=None, disk_size=None, disk_type=None, ephemeral_end_port=None, ephemeral_start_port=None, is_stateless=None, multiple_placement_groups=None, placement_property=None, primary=None, vm_image_offer=None, vm_image_publisher=None, vm_image_sku=None, vm_image_version=None, vm_size=None):
    '''
    Delete a managed cluster.
    '''
    return call_az("az sf managed-node-type create", locals())


def update(cluster_name, resource_group, application_end_port=None, application_start_port=None, capacity=None, ephemeral_end_port=None, ephemeral_start_port=None, instance_count=None, placement_property=None):
    '''
    Update a managed cluster.
    '''
    return call_az("az sf managed-node-type update", locals())

