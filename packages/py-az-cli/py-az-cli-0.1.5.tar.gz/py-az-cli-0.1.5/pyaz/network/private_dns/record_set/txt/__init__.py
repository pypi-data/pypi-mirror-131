from ..... pyaz_utils import _call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of a TXT record set.
    '''
    return _call_az("az network private-dns record-set txt show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete a TXT record set and all associated records.
    '''
    return _call_az("az network private-dns record-set txt delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all TXT record sets in a zone.
    '''
    return _call_az("az network private-dns record-set txt list", locals())


def create(name, resource_group, zone_name, metadata=None, record_type=None, ttl=None):
    '''
    Create an empty TXT record set.
    '''
    return _call_az("az network private-dns record-set txt create", locals())


def add_record(record_set_name, resource_group, value, zone_name):
    '''
    Add a TXT record.
    '''
    return _call_az("az network private-dns record-set txt add-record", locals())


def remove_record(record_set_name, resource_group, value, zone_name, keep_empty_record_set=None):
    '''
    Remove a TXT record from its record set.
    '''
    return _call_az("az network private-dns record-set txt remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, metadata=None, record_type=None, remove=None, set=None):
    '''
    Update a TXT record set.
    '''
    return _call_az("az network private-dns record-set txt update", locals())

