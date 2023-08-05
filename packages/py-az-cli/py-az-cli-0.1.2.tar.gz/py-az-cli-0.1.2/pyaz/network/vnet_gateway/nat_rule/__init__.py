from .... pyaz_utils import call_az

def add(external_mappings, gateway_name, internal_mappings, name, resource_group, ip_config_id=None, mode=None, no_wait=None, type=None):
    '''
    Add nat rule in a virtual network gateway
    '''
    return call_az("az network vnet-gateway nat-rule add", locals())


def list(gateway_name, resource_group):
    '''
    List nat rule for a virtual network gateway
    '''
    return call_az("az network vnet-gateway nat-rule list", locals())


def remove(gateway_name, name, resource_group, no_wait=None):
    '''
    Remove nat rule from a virtual network gateway
    '''
    return call_az("az network vnet-gateway nat-rule remove", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the vnet gateway nat rule is met.
    '''
    return call_az("az network vnet-gateway nat-rule wait", locals())

