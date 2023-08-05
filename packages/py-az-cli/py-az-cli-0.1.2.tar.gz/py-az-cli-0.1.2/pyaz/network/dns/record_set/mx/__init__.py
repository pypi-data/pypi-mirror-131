from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of an MX record set.
    '''
    return call_az("az network dns record-set mx show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete an MX record set and all associated records.
    '''
    return call_az("az network dns record-set mx delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all MX record sets in a zone.
    '''
    return call_az("az network dns record-set mx list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty MX record set.
    '''
    return call_az("az network dns record-set mx create", locals())


def add_record(exchange, preference, record_set_name, resource_group, zone_name, if_none_match=None, ttl=None):
    '''
    Add an MX record.
    '''
    return call_az("az network dns record-set mx add-record", locals())


def remove_record(exchange, preference, record_set_name, resource_group, zone_name, keep_empty_record_set=None):
    '''
    Remove an MX record from its record set.
    '''
    return call_az("az network dns record-set mx remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, if_none_match=None, metadata=None, record_type=None, remove=None, set=None, target_resource=None):
    '''
    Update an MX record set.
    '''
    return call_az("az network dns record-set mx update", locals())

