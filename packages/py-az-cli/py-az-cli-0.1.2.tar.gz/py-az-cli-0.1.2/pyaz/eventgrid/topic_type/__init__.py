from ... pyaz_utils import call_az

def list():
    '''
    List registered topic types.
    '''
    return call_az("az eventgrid topic-type list", locals())


def show(name):
    '''
    Get the details for a topic type.
    '''
    return call_az("az eventgrid topic-type show", locals())


def list_event_types(name):
    '''
    List the event types supported by a topic type.
    '''
    return call_az("az eventgrid topic-type list-event-types", locals())

