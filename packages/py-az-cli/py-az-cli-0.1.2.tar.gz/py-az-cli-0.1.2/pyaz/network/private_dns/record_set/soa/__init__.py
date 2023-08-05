from ..... pyaz_utils import call_az

def show(resource_group, zone_name, name=None, record_type=None):
    '''
    Get the details of an SOA record.
    '''
    return call_az("az network private-dns record-set soa show", locals())


def update(resource_group, zone_name, email=None, expire_time=None, host=None, minimum_ttl=None, refresh_time=None, retry_time=None, serial_number=None):
    '''
    Update properties of an SOA record.
    '''
    return call_az("az network private-dns record-set soa update", locals())

