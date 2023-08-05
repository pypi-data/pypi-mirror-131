from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of a CNAME record set.
    '''
    return call_az("az network dns record-set cname show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete a CNAME record set and its associated record.
    '''
    return call_az("az network dns record-set cname delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List the CNAME record set in a zone.
    '''
    return call_az("az network dns record-set cname list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty CNAME record set.
    '''
    return call_az("az network dns record-set cname create", locals())


def set_record(cname, record_set_name, resource_group, zone_name, if_none_match=None, ttl=None):
    '''
    Set the value of a CNAME record.
    '''
    return call_az("az network dns record-set cname set-record", locals())


def remove_record(cname, record_set_name, resource_group, zone_name, keep_empty_record_set=None):
    '''
    Remove a CNAME record from its record set.
    '''
    return call_az("az network dns record-set cname remove-record", locals())

