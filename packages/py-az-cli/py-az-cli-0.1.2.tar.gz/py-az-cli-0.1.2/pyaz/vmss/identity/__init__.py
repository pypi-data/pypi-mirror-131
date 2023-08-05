from ... pyaz_utils import call_az

def assign(name, resource_group, identities=None, role=None, scope=None):
    '''
    Enable managed service identity on a VMSS.
    '''
    return call_az("az vmss identity assign", locals())


def remove(name, resource_group, identities=None):
    '''
    Remove user assigned identities from a VM scaleset.
    '''
    return call_az("az vmss identity remove", locals())


def show(name, resource_group):
    '''
    display VM scaleset's managed identity info.
    '''
    return call_az("az vmss identity show", locals())

