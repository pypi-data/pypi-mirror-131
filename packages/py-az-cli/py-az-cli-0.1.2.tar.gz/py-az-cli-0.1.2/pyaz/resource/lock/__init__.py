from ... pyaz_utils import call_az

def create(lock_type, name, namespace=None, notes=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    Create a resource-level lock.
    '''
    return call_az("az resource lock create", locals())


def delete(ids=None, name=None, namespace=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    Delete a resource-level lock.
    '''
    return call_az("az resource lock delete", locals())


def list(filter_string=None, namespace=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    List lock information in the resource-level.
    '''
    return call_az("az resource lock list", locals())


def show(ids=None, name=None, namespace=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    Show the details of a resource-level lock
    '''
    return call_az("az resource lock show", locals())


def update(ids=None, lock_type=None, name=None, namespace=None, notes=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    Update a resource-level lock.
    '''
    return call_az("az resource lock update", locals())

