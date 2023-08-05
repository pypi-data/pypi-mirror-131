from .... pyaz_utils import call_az

def create(name, resource_group, server_name, subnet, ignore_missing_endpoint=None, vnet_name=None):
    '''
    Create a virtual network rule to allows access to a MySQL server.
    '''
    return call_az("az mysql server vnet-rule create", locals())


def delete(name, resource_group, server_name):
    return call_az("az mysql server vnet-rule delete", locals())


def show(name, resource_group, server_name):
    return call_az("az mysql server vnet-rule show", locals())


def list(resource_group, server_name):
    return call_az("az mysql server vnet-rule list", locals())


def update(name, resource_group, server_name, subnet, add=None, force_string=None, ignore_missing_endpoint=None, remove=None, set=None, vnet_name=None):
    '''
    Update a virtual network rule.
    '''
    return call_az("az mysql server vnet-rule update", locals())

