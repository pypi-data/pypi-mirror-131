from ... pyaz_utils import call_az
from . import event_subscription


def show(name, resource_group):
    '''
    Get the details of a system topic.
    '''
    return call_az("az eventgrid system-topic show", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a system topic.
    '''
    return call_az("az eventgrid system-topic delete", locals())


def list(odata_query=None, resource_group=None):
    '''
    List available system topics.
    '''
    return call_az("az eventgrid system-topic list", locals())


def create(name, resource_group, source, topic_type, identity=None, location=None, tags=None):
    '''
    Create a system topic.
    '''
    return call_az("az eventgrid system-topic create", locals())


def update(name, resource_group, identity=None, tags=None):
    '''
    Update a system topic.
    '''
    return call_az("az eventgrid system-topic update", locals())

