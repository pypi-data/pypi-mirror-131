from ... pyaz_utils import call_az
from . import site, sku


def create(name, resource_group, scale_unit, vendor, version, vhub, asn=None, boot_strap_config_blobs=None, cloud_init_config=None, cloud_init_config_blobs=None, location=None, tags=None):
    '''
    Create an Azure network virtual appliance.
    '''
    return call_az("az network virtual-appliance create", locals())


def update(name, resource_group, add=None, asn=None, cloud_init_config=None, force_string=None, remove=None, set=None):
    '''
    Update an Azure network virtual appliance.
    '''
    return call_az("az network virtual-appliance update", locals())


def show(name, resource_group, expand=None):
    '''
    Show the detail of an Azure network virtual appliance.
    '''
    return call_az("az network virtual-appliance show", locals())


def list(resource_group=None):
    '''
    List all Azure network virtual appliance.
    '''
    return call_az("az network virtual-appliance list", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete an Azure network virtual appliance.
    '''
    return call_az("az network virtual-appliance delete", locals())

