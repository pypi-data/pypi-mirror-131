from .. pyaz_utils import call_az
from . import builder


def create(name, resource_group, source, data_disk_caching=None, data_disk_sources=None, edge_zone=None, hyper_v_generation=None, location=None, os_disk_caching=None, os_type=None, storage_sku=None, tags=None, zone_resilient=None):
    '''
    Create a custom Virtual Machine Image from managed disks or snapshots.
    '''
    return call_az("az image create", locals())


def list(resource_group=None):
    '''
    List custom VM images.
    '''
    return call_az("az image list", locals())


def show(name, resource_group, expand=None):
    return call_az("az image show", locals())


def delete(name, resource_group):
    return call_az("az image delete", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update custom VM images.
    '''
    return call_az("az image update", locals())

