from ... pyaz_utils import _call_az

def add(name, ip_address=None, no_wait=None, resource_group=None, subnet=None, vnet_name=None):
    return _call_az("az keyvault network-rule add", locals())


def remove(name, ip_address=None, no_wait=None, resource_group=None, subnet=None, vnet_name=None):
    return _call_az("az keyvault network-rule remove", locals())


def list(name, resource_group=None):
    return _call_az("az keyvault network-rule list", locals())


def wait(name, created=None, custom=None, deleted=None, exists=None, interval=None, resource_group=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the vault is met.
    '''
    return _call_az("az keyvault network-rule wait", locals())

