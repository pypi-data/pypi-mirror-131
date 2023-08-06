from ... pyaz_utils import _call_az

def assign(name, resource_group, identities=None, role=None, scope=None):
    '''
    Enable managed service identity on a VM.
    '''
    return _call_az("az vm identity assign", locals())


def remove(name, resource_group, identities=None):
    '''
    Remove managed service identities from a VM.
    '''
    return _call_az("az vm identity remove", locals())


def show(name, resource_group):
    '''
    display VM's managed identity info.
    '''
    return _call_az("az vm identity show", locals())

