from .... pyaz_utils import call_az

def create(autoscale_name, count, name, resource_group, timezone, copy_rules=None, end=None, max_count=None, min_count=None, recurrence=None, start=None):
    '''
    Create a fixed or recurring autoscale profile.
    '''
    return call_az("az monitor autoscale profile create", locals())


def list(autoscale_name, resource_group):
    '''
    List autoscale profiles.
    '''
    return call_az("az monitor autoscale profile list", locals())


def show(autoscale_name, name, resource_group):
    '''
    Show details of an autoscale profile.
    '''
    return call_az("az monitor autoscale profile show", locals())


def delete(autoscale_name, name, resource_group):
    '''
    Delete an autoscale profile.
    '''
    return call_az("az monitor autoscale profile delete", locals())


def list_timezones(offset=None, search_query=None):
    '''
    Look up time zone information.
    '''
    return call_az("az monitor autoscale profile list-timezones", locals())

