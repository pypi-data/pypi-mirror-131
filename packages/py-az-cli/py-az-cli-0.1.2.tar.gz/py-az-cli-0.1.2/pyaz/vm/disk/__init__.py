from ... pyaz_utils import call_az

def attach(name, resource_group, vm_name, caching=None, enable_write_accelerator=None, lun=None, new=None, size_gb=None, sku=None):
    '''
    Attach a managed persistent disk to a VM. Please note that --ids only supports one disk.
    '''
    return call_az("az vm disk attach", locals())


def detach(name, resource_group, vm_name):
    '''
    Detach a managed disk from a VM.
    '''
    return call_az("az vm disk detach", locals())

