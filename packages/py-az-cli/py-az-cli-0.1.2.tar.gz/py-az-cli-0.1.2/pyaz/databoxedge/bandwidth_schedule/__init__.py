from ... pyaz_utils import call_az

def list(device_name, resource_group):
    '''
    Get all the bandwidth schedules for a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge bandwidth-schedule list", locals())


def show(device_name, name, resource_group):
    '''
    Get the properties of the specified bandwidth schedule.
    '''
    return call_az("az databoxedge bandwidth-schedule show", locals())


def create(days, device_name, name, rate_in_mbps, resource_group, start, stop, no_wait=None):
    '''
    Create a bandwidth schedule.
    '''
    return call_az("az databoxedge bandwidth-schedule create", locals())


def update(days, device_name, name, rate_in_mbps, resource_group, start, stop, add=None, force_string=None, no_wait=None, remove=None, set=None):
    '''
    Update a bandwidth schedule.
    '''
    return call_az("az databoxedge bandwidth-schedule update", locals())


def delete(device_name, name, resource_group, no_wait=None, yes=None):
    '''
    Delete the specified bandwidth schedule.
    '''
    return call_az("az databoxedge bandwidth-schedule delete", locals())


def wait(device_name, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the databoxedge bandwidth-schedule is met.
    '''
    return call_az("az databoxedge bandwidth-schedule wait", locals())

