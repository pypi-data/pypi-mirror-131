from ... pyaz_utils import call_az

def attach(resource_group, vmss_name, caching=None, disk=None, instance_id=None, lun=None, size_gb=None, sku=None):
    '''
    Attach managed data disks to a scale set or its instances.
    '''
    return call_az("az vmss disk attach", locals())


def detach(lun, resource_group, vmss_name, instance_id=None):
    '''
    Detach managed data disks from a scale set or its instances.
    '''
    return call_az("az vmss disk detach", locals())

