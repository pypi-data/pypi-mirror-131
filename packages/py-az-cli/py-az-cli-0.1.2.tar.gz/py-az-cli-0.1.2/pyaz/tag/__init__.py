from .. pyaz_utils import call_az

def list(resource_id=None):
    '''
    List the entire set of tags on a specific resource.
    '''
    return call_az("az tag list", locals())


def create(name=None, resource_id=None, tags=None):
    '''
    Create tags on a specific resource.
    '''
    return call_az("az tag create", locals())


def delete(name=None, resource_id=None, yes=None):
    '''
    Delete tags on a specific resource.
    '''
    return call_az("az tag delete", locals())


def update(operation, resource_id, tags):
    '''
    Selectively update the set of tags on a specific resource.
    '''
    return call_az("az tag update", locals())


def add_value(name, value):
    '''
    Create a tag value.
    '''
    return call_az("az tag add-value", locals())


def remove_value(name, value):
    return call_az("az tag remove-value", locals())

