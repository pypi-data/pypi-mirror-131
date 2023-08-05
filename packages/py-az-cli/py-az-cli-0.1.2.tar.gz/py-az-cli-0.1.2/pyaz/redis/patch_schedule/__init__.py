from ... pyaz_utils import call_az

def create(name, resource_group, schedule_entries):
    '''
    Create patching schedule for Redis cache.
    '''
    return call_az("az redis patch-schedule create", locals())


def update(name, resource_group, schedule_entries):
    '''
    Update the patching schedule for Redis cache.
    '''
    return call_az("az redis patch-schedule update", locals())


def delete(name, resource_group):
    '''
    Deletes the patching schedule of a redis cache.
    '''
    return call_az("az redis patch-schedule delete", locals())


def show(name, resource_group):
    '''
    Gets the patching schedule of a redis cache.
    '''
    return call_az("az redis patch-schedule show", locals())

