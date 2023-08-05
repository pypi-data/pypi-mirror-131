from .... pyaz_utils import call_az
from . import a, aaaa, caa, cname, mx, ns, ptr, soa, srv, txt


def list(resource_group, zone_name, record_type=None):
    '''
    List all record sets within a DNS zone.
    '''
    return call_az("az network dns record-set list", locals())

