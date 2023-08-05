from ... pyaz_utils import call_az
from . import image


def delete(name, resource_group, vmss_name, no_wait=None):
    '''
    Delete an extension from a VMSS.
    '''
    return call_az("az vmss extension delete", locals())


def show(name, resource_group, vmss_name):
    '''
    Show details on a VMSS extension.
    '''
    return call_az("az vmss extension show", locals())


def set(name, publisher, resource_group, vmss_name, enable_auto_upgrade=None, extension_instance_name=None, force_update=None, no_auto_upgrade_minor_version=None, no_wait=None, protected_settings=None, provision_after_extensions=None, settings=None, version=None):
    '''
    Add an extension to a VMSS or update an existing extension.
    '''
    return call_az("az vmss extension set", locals())


def list(resource_group, vmss_name):
    '''
    List extensions associated with a VMSS.
    '''
    return call_az("az vmss extension list", locals())


def upgrade(name, resource_group, no_wait=None):
    '''
    Upgrade all extensions for all VMSS instances to the latest version.
    '''
    return call_az("az vmss extension upgrade", locals())

