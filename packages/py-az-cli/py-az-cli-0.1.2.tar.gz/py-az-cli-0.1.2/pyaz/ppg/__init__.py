from .. pyaz_utils import call_az

def show(name, resource_group, include_colocation_status=None):
    '''
    Get a proximity placement group
    '''
    return call_az("az ppg show", locals())


def create(name, resource_group, location=None, tags=None, type=None):
    '''
    Create a proximity placement group
    '''
    return call_az("az ppg create", locals())


def list(resource_group=None):
    '''
    List proximity placement groups
    '''
    return call_az("az ppg list", locals())


def update(name, resource_group, add=None, force_string=None, include_colocation_status=None, remove=None, set=None):
    '''
    Update a proximity placement group
    '''
    return call_az("az ppg update", locals())


def delete(name, resource_group):
    return call_az("az ppg delete", locals())

