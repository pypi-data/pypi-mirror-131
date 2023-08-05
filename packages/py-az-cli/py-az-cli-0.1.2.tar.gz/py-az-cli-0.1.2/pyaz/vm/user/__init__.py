from ... pyaz_utils import call_az

def update(name, resource_group, username, no_wait=None, password=None, ssh_key_value=None):
    '''
    Update a user account.
    '''
    return call_az("az vm user update", locals())


def delete(name, resource_group, username, no_wait=None):
    '''
    Delete a user account from a VM.
    '''
    return call_az("az vm user delete", locals())


def reset_ssh(name, resource_group, no_wait=None):
    '''
    Reset the SSH configuration on a VM.
    '''
    return call_az("az vm user reset-ssh", locals())

