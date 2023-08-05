from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of an NS record set.
    '''
    return call_az("az network dns record-set ns show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete an NS record set and all associated records.
    '''
    return call_az("az network dns record-set ns delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all NS record sets in a zone.
    '''
    return call_az("az network dns record-set ns list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty NS record set.
    '''
    return call_az("az network dns record-set ns create", locals())


def add_record(nsdname, record_set_name, resource_group, zone_name, if_none_match=None, subscriptionid=None, ttl=None):
    '''
    Add an NS record.
    '''
    return call_az("az network dns record-set ns add-record", locals())


def remove_record(nsdname, record_set_name, resource_group, zone_name, keep_empty_record_set=None):
    '''
    Remove an NS record from its record set.
    '''
    return call_az("az network dns record-set ns remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, if_none_match=None, metadata=None, record_type=None, remove=None, set=None, target_resource=None):
    '''
    Update an NS record set.
    '''
    return call_az("az network dns record-set ns update", locals())

