from ..... pyaz_utils import call_az

def delete(name, resource_group, zone_name, if_match=None, no_wait=None, yes=None):
    '''
    Delete a virtual network link to the specified Private DNS zone.
    '''
    return call_az("az network private-dns link vnet delete", locals())


def show(name, resource_group, zone_name):
    '''
    Get a virtual network link to the specified Private DNS zone.
    '''
    return call_az("az network private-dns link vnet show", locals())


def list(resource_group, zone_name, top=None):
    '''
    List the virtual network links to the specified Private DNS zone.
    '''
    return call_az("az network private-dns link vnet list", locals())


def create(name, registration_enabled, resource_group, virtual_network, zone_name, no_wait=None, tags=None):
    '''
    Create a virtual network link to the specified Private DNS zone.
    '''
    return call_az("az network private-dns link vnet create", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, no_wait=None, registration_enabled=None, remove=None, set=None, tags=None):
    '''
    Update a virtual network link's properties. Does not modify virtual network within the link.
    '''
    return call_az("az network private-dns link vnet update", locals())


def wait(name, resource_group, zone_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the virtual network link to the specified Private DNS zone is met.
    '''
    return call_az("az network private-dns link vnet wait", locals())

