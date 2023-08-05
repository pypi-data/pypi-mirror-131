from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of a TXT record set.
    '''
    return call_az("az network dns record-set txt show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete a TXT record set and all associated records.
    '''
    return call_az("az network dns record-set txt delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all TXT record sets in a zone.
    '''
    return call_az("az network dns record-set txt list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty TXT record set.
    '''
    return call_az("az network dns record-set txt create", locals())


def add_record(record_set_name, resource_group, value, zone_name, if_none_match=None):
    '''
    Add a TXT record.
    '''
    return call_az("az network dns record-set txt add-record", locals())


def remove_record(record_set_name, resource_group, value, zone_name, keep_empty_record_set=None):
    '''
    Remove a TXT record from its record set.
    '''
    return call_az("az network dns record-set txt remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, if_none_match=None, metadata=None, record_type=None, remove=None, set=None, target_resource=None):
    '''
    Update a TXT record set.
    '''
    return call_az("az network dns record-set txt update", locals())

