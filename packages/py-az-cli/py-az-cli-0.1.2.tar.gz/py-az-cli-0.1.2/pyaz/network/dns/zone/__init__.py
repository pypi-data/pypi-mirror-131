from .... pyaz_utils import call_az

def delete(name, resource_group, if_match=None, yes=None):
    '''
    Delete a DNS zone and all associated records.
    '''
    return call_az("az network dns zone delete", locals())


def show(name, resource_group):
    '''
    Get a DNS zone parameters. Does not show DNS records within the zone.
    '''
    return call_az("az network dns zone show", locals())


def list(resource_group=None):
    '''
    List DNS zones.
    '''
    return call_az("az network dns zone list", locals())


def import_(file_name, name, resource_group):
    '''
    Create a DNS zone using a DNS zone file.
    '''
    return call_az("az network dns zone import", locals())


def export(name, resource_group, file_name=None):
    '''
    Export a DNS zone as a DNS zone file.
    '''
    return call_az("az network dns zone export", locals())


def create(name, resource_group, if_none_match=None, parent_name=None, registration_vnets=None, resolution_vnets=None, tags=None, zone_type=None):
    '''
    Create a DNS zone.
    '''
    return call_az("az network dns zone create", locals())


def update(name, resource_group, add=None, force_string=None, if_match=None, registration_vnets=None, remove=None, resolution_vnets=None, set=None, tags=None, zone_type=None):
    '''
    Update a DNS zone properties. Does not modify DNS records within the zone.
    '''
    return call_az("az network dns zone update", locals())

