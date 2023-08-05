from ... pyaz_utils import call_az

def enable(disk_encryption_keyvault, name, resource_group, force=None, key_encryption_algorithm=None, key_encryption_key=None, key_encryption_keyvault=None, volume_type=None):
    '''
    Encrypt a VMSS with managed disks.
    '''
    return call_az("az vmss encryption enable", locals())


def disable(name, resource_group, force=None, volume_type=None):
    '''
    Disable the encryption on a VMSS with managed disks.
    '''
    return call_az("az vmss encryption disable", locals())


def show(name, resource_group):
    '''
    Show encryption status.
    '''
    return call_az("az vmss encryption show", locals())

