from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of a PTR record set.
    '''
    return call_az("az network private-dns record-set ptr show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete a PTR record set and all associated records.
    '''
    return call_az("az network private-dns record-set ptr delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all PTR record sets in a zone.
    '''
    return call_az("az network private-dns record-set ptr list", locals())


def create(name, resource_group, zone_name, metadata=None, record_type=None, ttl=None):
    '''
    Create an empty PTR record set.
    '''
    return call_az("az network private-dns record-set ptr create", locals())


def add_record(ptrdname, record_set_name, resource_group, zone_name):
    '''
    Add a PTR record.
    '''
    return call_az("az network private-dns record-set ptr add-record", locals())


def remove_record(ptrdname, record_set_name, resource_group, zone_name, keep_empty_record_set=None):
    '''
    Remove a PTR record from its record set.
    '''
    return call_az("az network private-dns record-set ptr remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, metadata=None, record_type=None, remove=None, set=None):
    '''
    Update a PTR record set.
    '''
    return call_az("az network private-dns record-set ptr update", locals())

