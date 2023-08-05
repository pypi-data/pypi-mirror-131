from ... pyaz_utils import call_az

def attach(resource_group, vm_name, caching=None, lun=None, name=None, new=None, size_gb=None, vhd_uri=None):
    '''
    Attach an unmanaged persistent disk to a VM.
    '''
    return call_az("az vm unmanaged-disk attach", locals())


def detach(name, resource_group, vm_name):
    '''
    Detach an unmanaged disk from a VM.
    '''
    return call_az("az vm unmanaged-disk detach", locals())


def list(resource_group, vm_name):
    '''
    List unmanaged disks of a VM.
    '''
    return call_az("az vm unmanaged-disk list", locals())

