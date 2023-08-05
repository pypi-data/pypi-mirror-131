from .. pyaz_utils import call_az

def create(name, resource_group, location=None, no_wait=None, tags=None):
    '''
    Create a disk access resource.
    '''
    return call_az("az disk-access create", locals())


def update(name, resource_group, add=None, force_string=None, no_wait=None, remove=None, set=None, tags=None):
    '''
    Update a disk access resource.
    '''
    return call_az("az disk-access update", locals())


def show(name, resource_group):
    '''
    Get information of a disk access resource.
    '''
    return call_az("az disk-access show", locals())


def list(resource_group=None):
    '''
    List disk access resources.
    '''
    return call_az("az disk-access list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a disk access is met.
    '''
    return call_az("az disk-access wait", locals())


def delete(name, resource_group):
    '''
    Delete a disk access resource.
    '''
    return call_az("az disk-access delete", locals())

