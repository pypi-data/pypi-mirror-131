from ..... pyaz_utils import call_az

def show(name, partner_namespace_name, resource_group):
    '''
    Get the details of an event channel under a partner namespace.
    '''
    return call_az("az eventgrid partner namespace event-channel show", locals())


def delete(name, partner_namespace_name, resource_group, yes=None):
    '''
    Delete a partner namespace.
    '''
    return call_az("az eventgrid partner namespace event-channel delete", locals())


def list(partner_namespace_name, resource_group, odata_query=None):
    '''
    List available partner event-channels.
    '''
    return call_az("az eventgrid partner namespace event-channel list", locals())


def create(destination_resource_group_name, destination_subscription_id, destination_topic_name, name, partner_namespace_name, resource_group, source, activation_expiration_date=None, partner_topic_description=None, publisher_filter=None):
    '''
    Create an event channel under a partner namespace.
    '''
    return call_az("az eventgrid partner namespace event-channel create", locals())

