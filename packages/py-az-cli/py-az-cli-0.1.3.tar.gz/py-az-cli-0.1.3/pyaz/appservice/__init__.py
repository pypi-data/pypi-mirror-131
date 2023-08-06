from .. pyaz_utils import _call_az
from . import ase, domain, hybrid_connection, plan, vnet_integration


def list_locations(sku, linux_workers_enabled=None):
    '''
    List regions where a plan sku is available.
    '''
    return _call_az("az appservice list-locations", locals())

