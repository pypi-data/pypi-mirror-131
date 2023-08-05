from ... pyaz_utils import call_az
from . import group


def show(host_group, name, resource_group):
    '''
    Get the details of a dedicated host.
    '''
    return call_az("az vm host show", locals())


def get_instance_view(host_group, name, resource_group):
    '''
    Get instance information about a dedicated host.
    '''
    return call_az("az vm host get-instance-view", locals())


def create(host_group, name, resource_group, sku, auto_replace=None, license_type=None, location=None, platform_fault_domain=None, tags=None):
    '''
    Create a dedicated host.
    '''
    return call_az("az vm host create", locals())


def list(host_group, resource_group):
    '''
    List dedicated hosts.
    '''
    return call_az("az vm host list", locals())


def update(host_group, name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a dedicated host.
    '''
    return call_az("az vm host update", locals())


def delete(host_group, name, resource_group, yes=None):
    return call_az("az vm host delete", locals())

