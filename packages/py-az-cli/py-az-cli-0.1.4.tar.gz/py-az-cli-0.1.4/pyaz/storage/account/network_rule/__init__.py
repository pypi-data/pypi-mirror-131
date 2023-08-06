from .... pyaz_utils import _call_az

def add(account_name, action=None, ip_address=None, resource_group=None, resource_id=None, subnet=None, tenant_id=None, vnet_name=None):
    '''
    Add a network rule.
    '''
    return _call_az("az storage account network-rule add", locals())


def list(account_name, resource_group=None):
    '''
    List network rules.
    '''
    return _call_az("az storage account network-rule list", locals())


def remove(account_name, ip_address=None, resource_group=None, resource_id=None, subnet=None, tenant_id=None, vnet_name=None):
    '''
    Remove a network rule.
    '''
    return _call_az("az storage account network-rule remove", locals())

