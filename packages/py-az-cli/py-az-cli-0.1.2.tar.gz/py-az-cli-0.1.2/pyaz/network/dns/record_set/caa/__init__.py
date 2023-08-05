from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of a CAA record set.
    '''
    return call_az("az network dns record-set caa show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete a CAA record set and all associated records.
    '''
    return call_az("az network dns record-set caa delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all CAA record sets in a zone.
    '''
    return call_az("az network dns record-set caa list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty CAA record set.
    '''
    return call_az("az network dns record-set caa create", locals())


def add_record(flags, record_set_name, resource_group, tag, value, zone_name, if_none_match=None, ttl=None):
    '''
    Add a CAA record.
    '''
    return call_az("az network dns record-set caa add-record", locals())


def remove_record(flags, record_set_name, resource_group, tag, value, zone_name, keep_empty_record_set=None):
    '''
    Remove a CAA record from its record set.
    '''
    return call_az("az network dns record-set caa remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, if_none_match=None, metadata=None, record_type=None, remove=None, set=None, target_resource=None):
    '''
    Update a CAA record set.
    '''
    return call_az("az network dns record-set caa update", locals())

