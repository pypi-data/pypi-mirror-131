from .. pyaz_utils import call_az

def list(resource_group=None):
    '''
    List all of the SSH public keys.
    '''
    return call_az("az sshkey list", locals())


def show(name, resource_group):
    '''
    Retrieve information about an SSH public key.
    '''
    return call_az("az sshkey show", locals())


def create(name, resource_group, location=None, public_key=None, tags=None):
    '''
    Create a new SSH public key resource.
    '''
    return call_az("az sshkey create", locals())


def update(name, resource_group, public_key=None, tags=None):
    '''
    Update an SSH public key resource.
    '''
    return call_az("az sshkey update", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete an SSH public key.
    '''
    return call_az("az sshkey delete", locals())

