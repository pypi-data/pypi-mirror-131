from ... pyaz_utils import call_az
from . import alert


def list(caller=None, correlation_id=None, end_time=None, filters=None, max_events=None, namespace=None, offset=None, resource_group=None, resource_id=None, select=None, start_time=None, status=None):
    '''
    List and query activity log events.
    '''
    return call_az("az monitor activity-log list", locals())


def list_categories():
    '''
    List the event categories of activity logs.
    '''
    return call_az("az monitor activity-log list-categories", locals())

