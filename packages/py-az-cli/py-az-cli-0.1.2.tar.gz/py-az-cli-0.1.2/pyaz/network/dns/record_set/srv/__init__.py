from ..... pyaz_utils import call_az

def show(name, resource_group, zone_name, record_type=None):
    '''
    Get the details of an SRV record set.
    '''
    return call_az("az network dns record-set srv show", locals())


def delete(name, resource_group, zone_name, if_match=None, record_type=None, yes=None):
    '''
    Delete an SRV record set and all associated records.
    '''
    return call_az("az network dns record-set srv delete", locals())


def list(resource_group, zone_name, record_type=None):
    '''
    List all SRV record sets in a zone.
    '''
    return call_az("az network dns record-set srv list", locals())


def create(name, resource_group, zone_name, if_match=None, if_none_match=None, metadata=None, record_set_type=None, target_resource=None, ttl=None):
    '''
    Create an empty SRV record set.
    '''
    return call_az("az network dns record-set srv create", locals())


def add_record(port, priority, record_set_name, resource_group, target, weight, zone_name, if_none_match=None):
    '''
    Add an SRV record.
    '''
    return call_az("az network dns record-set srv add-record", locals())


def remove_record(port, priority, record_set_name, resource_group, target, weight, zone_name, keep_empty_record_set=None):
    '''
    Remove an SRV record from its record set.
    '''
    return call_az("az network dns record-set srv remove-record", locals())


def update(name, resource_group, zone_name, add=None, force_string=None, if_match=None, if_none_match=None, metadata=None, record_type=None, remove=None, set=None, target_resource=None):
    '''
    Update an SRV record set.
    '''
    return call_az("az network dns record-set srv update", locals())

