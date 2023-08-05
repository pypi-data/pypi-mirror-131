from .. pyaz_utils import call_az

def create(key_url, name, resource_group, source_vault, enable_auto_key_rotation=None, encryption_type=None, location=None, no_wait=None, tags=None):
    '''
    Create a disk encryption set.
    '''
    return call_az("az disk-encryption-set create", locals())


def delete(name, resource_group):
    '''
    Delete a disk encryption set.
    '''
    return call_az("az disk-encryption-set delete", locals())


def update(name, resource_group, add=None, enable_auto_key_rotation=None, force_string=None, key_url=None, remove=None, set=None, source_vault=None):
    '''
    Update a disk encryption set.
    '''
    return call_az("az disk-encryption-set update", locals())


def show(name, resource_group):
    '''
    Get information of a disk encryption sets.
    '''
    return call_az("az disk-encryption-set show", locals())


def list(resource_group=None):
    '''
    List disk encryption sets.
    '''
    return call_az("az disk-encryption-set list", locals())


def list_associated_resources(name, resource_group):
    return call_az("az disk-encryption-set list-associated-resources", locals())

