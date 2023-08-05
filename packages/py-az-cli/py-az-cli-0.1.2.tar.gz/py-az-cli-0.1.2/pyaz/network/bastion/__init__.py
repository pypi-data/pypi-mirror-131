from ... pyaz_utils import call_az

def create(name, public_ip_address, resource_group, vnet_name, location=None, scale_units=None, sku=None, tags=None):
    '''
    Create a Azure bastion host machine.
    '''
    return call_az("az network bastion create", locals())


def show(name, resource_group):
    '''
    Show a Azure bastion host machine.
    '''
    return call_az("az network bastion show", locals())


def list(resource_group=None):
    '''
    List all Azure bastion host machines.
    '''
    return call_az("az network bastion list", locals())


def ssh(auth_type, name, resource_group, target_resource_id, resource_port=None, ssh_key=None, username=None):
    '''
    SSH to a virtual machine using Tunneling from Azure Bastion.
    '''
    return call_az("az network bastion ssh", locals())


def rdp(name, resource_group, target_resource_id, resource_port=None):
    '''
    RDP to target Virtual Machine using Tunneling from Azure Bastion.
    '''
    return call_az("az network bastion rdp", locals())


def tunnel(name, port, resource_group, resource_port, target_resource_id, timeout=None):
    '''
    Show a Azure bastion host machine.
    '''
    return call_az("az network bastion tunnel", locals())


def delete(name, resource_group):
    '''
    Delete a Azure bastion host machine.
    '''
    return call_az("az network bastion delete", locals())

