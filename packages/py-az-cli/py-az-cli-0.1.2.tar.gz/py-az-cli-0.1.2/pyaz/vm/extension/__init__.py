from ... pyaz_utils import call_az
from . import image


def delete(name, resource_group, vm_name, no_wait=None):
    '''
    Remove an extension attached to a VM.
    '''
    return call_az("az vm extension delete", locals())


def show(name, resource_group, vm_name, expand=None):
    '''
    Display information about extensions attached to a VM.
    '''
    return call_az("az vm extension show", locals())


def set(name, publisher, resource_group, vm_name, enable_auto_upgrade=None, extension_instance_name=None, force_update=None, no_auto_upgrade_minor_version=None, no_wait=None, protected_settings=None, settings=None, version=None):
    '''
    Set extensions for a VM.
    '''
    return call_az("az vm extension set", locals())


def list(resource_group, vm_name):
    '''
    List the extensions attached to a VM.
    '''
    return call_az("az vm extension list", locals())


def wait(name, resource_group, vm_name, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a virtual machine extension is met.
    '''
    return call_az("az vm extension wait", locals())

