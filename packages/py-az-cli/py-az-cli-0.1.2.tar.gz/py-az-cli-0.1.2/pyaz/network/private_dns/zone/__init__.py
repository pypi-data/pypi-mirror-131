from .... pyaz_utils import call_az

def delete(name, resource_group, if_match=None, no_wait=None, yes=None):
    '''
    Delete a Private DNS zone.
    '''
    return call_az("az network private-dns zone delete", locals())


def show(name, resource_group):
    '''
    Get a Private DNS zone.
    '''
    return call_az("az network private-dns zone show", locals())


def list(resource_group=None):
    '''
    List Private DNS zones.
    '''
    return call_az("az network private-dns zone list", locals())


def import_(file_name, name, resource_group):
    '''
    Create a Private DNS zone using a DNS zone file.
    '''
    return call_az("az network private-dns zone import", locals())


def export(name, resource_group, file_name=None):
    '''
    Export a Private DNS zone as a DNS zone file.
    '''
    return call_az("az network private-dns zone export", locals())


def create(name, resource_group, no_wait=None, tags=None):
    '''
    Create a Private DNS zone.
    '''
    return call_az("az network private-dns zone create", locals())


def update(name, resource_group, add=None, force_string=None, if_match=None, no_wait=None, remove=None, set=None, tags=None):
    '''
    Update a Private DNS zone's properties. Does not modify Private DNS records or virtual network links within the zone.
    '''
    return call_az("az network private-dns zone update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the Private DNS zone is met.
    '''
    return call_az("az network private-dns zone wait", locals())

