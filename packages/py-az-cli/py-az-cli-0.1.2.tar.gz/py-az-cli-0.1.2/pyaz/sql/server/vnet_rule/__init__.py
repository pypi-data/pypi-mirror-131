from .... pyaz_utils import call_az

def create(name, resource_group, server, subnet, ignore_missing_endpoint=None, vnet_name=None):
    '''
    Create a virtual network rule to allows access to an Azure SQL server.
    '''
    return call_az("az sql server vnet-rule create", locals())


def show(name, resource_group, server):
    return call_az("az sql server vnet-rule show", locals())


def list(resource_group, server):
    return call_az("az sql server vnet-rule list", locals())


def delete(name, resource_group, server):
    return call_az("az sql server vnet-rule delete", locals())


def update(name, resource_group, server, subnet, ignore_missing_endpoint=None):
    '''
    Update a virtual network rule.
    '''
    return call_az("az sql server vnet-rule update", locals())

