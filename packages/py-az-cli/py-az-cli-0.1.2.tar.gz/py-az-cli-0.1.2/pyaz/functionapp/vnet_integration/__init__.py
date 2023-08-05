from ... pyaz_utils import call_az

def add(name, resource_group, subnet, vnet, skip_delegation_check=None, slot=None):
    '''
    Add a regional virtual network integration to a functionapp
    '''
    return call_az("az functionapp vnet-integration add", locals())


def list(name, resource_group, slot=None):
    '''
    list the virtual network integrations on a functionapp
    '''
    return call_az("az functionapp vnet-integration list", locals())


def remove(name, resource_group, slot=None):
    '''
    remove a regional virtual network integration from functionapp
    '''
    return call_az("az functionapp vnet-integration remove", locals())

