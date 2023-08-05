from ..... pyaz_utils import call_az

def update(group_name, name, resource_group, add=None, force_string=None, remove=None, set=None, sqlvms=None):
    '''
    Updates an availability group listener.
    '''
    return call_az("az sql vm group ag-listener update", locals())


def show(group_name, name, resource_group):
    return call_az("az sql vm group ag-listener show", locals())


def list(group_name, resource_group):
    return call_az("az sql vm group ag-listener list", locals())


def delete(group_name, name, resource_group, yes=None):
    return call_az("az sql vm group ag-listener delete", locals())


def create(ag_name, group_name, ip_address, load_balancer, name, probe_port, resource_group, sqlvms, subnet, port=None, public_ip=None, vnet_name=None):
    '''
    Creates an availability group listener.
    '''
    return call_az("az sql vm group ag-listener create", locals())

