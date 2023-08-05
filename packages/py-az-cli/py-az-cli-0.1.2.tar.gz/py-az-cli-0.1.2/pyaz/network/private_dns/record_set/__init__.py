from .... pyaz_utils import call_az
from . import a, aaaa, cname, mx, ptr, soa, srv, txt


def list(resource_group, zone_name, record_type=None):
    '''
    List all record sets within a Private DNS zone.
    '''
    return call_az("az network private-dns record-set list", locals())

