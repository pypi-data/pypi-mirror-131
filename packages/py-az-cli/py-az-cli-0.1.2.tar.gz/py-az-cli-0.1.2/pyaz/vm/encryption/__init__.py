from ... pyaz_utils import call_az

def enable(disk_encryption_keyvault, name, resource_group, aad_client_cert_thumbprint=None, aad_client_id=None, aad_client_secret=None, encrypt_format_all=None, force=None, key_encryption_algorithm=None, key_encryption_key=None, key_encryption_keyvault=None, volume_type=None):
    '''
    Enable disk encryption on the OS disk and/or data disks. Encrypt mounted disks.
    '''
    return call_az("az vm encryption enable", locals())


def disable(name, resource_group, force=None, volume_type=None):
    '''
    Disable disk encryption on the OS disk and/or data disks. Decrypt mounted disks.
    '''
    return call_az("az vm encryption disable", locals())


def show(name, resource_group):
    '''
    Show encryption status.
    '''
    return call_az("az vm encryption show", locals())

