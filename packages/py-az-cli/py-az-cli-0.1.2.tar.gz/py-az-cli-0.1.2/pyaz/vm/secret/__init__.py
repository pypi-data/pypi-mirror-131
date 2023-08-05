from ... pyaz_utils import call_az

def format(secrets, certificate_store=None, keyvault=None, resource_group=None):
    '''
    Transform secrets into a form that can be used by VMs and VMSSes.
    '''
    return call_az("az vm secret format", locals())


def add(certificate, keyvault, name, resource_group, certificate_store=None):
    '''
    Add a secret to a VM.
    '''
    return call_az("az vm secret add", locals())


def list(name, resource_group):
    '''
    List secrets on a VM.
    '''
    return call_az("az vm secret list", locals())


def remove(keyvault, name, resource_group, certificate=None):
    '''
    Remove a secret from a VM.
    '''
    return call_az("az vm secret remove", locals())

