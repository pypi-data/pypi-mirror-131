from ... pyaz_utils import _call_az

def list(resource_group, vmss_name):
    return _call_az("az vmss nic list", locals())


def list_vm_nics(instance_id, resource_group, vmss_name):
    return _call_az("az vmss nic list-vm-nics", locals())


def show(instance_id, name, resource_group, vmss_name, expand=None):
    return _call_az("az vmss nic show", locals())

