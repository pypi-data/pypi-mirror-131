from ..... pyaz_utils import call_az

def create(name, namespace_name, resource_group, subscription_name, topic_name, action_compatibility_level=None, action_sql_expression=None, content_type=None, correlation_id=None, enable_action_preprocessing=None, enable_correlation_preprocessing=None, enable_sql_preprocessing=None, filter_sql_expression=None, label=None, message_id=None, reply_to=None, reply_to_session_id=None, session_id=None, to=None):
    '''
    Create the ServiceBus Rule for Subscription
    '''
    return call_az("az servicebus topic subscription rule create", locals())


def show(name, namespace_name, resource_group, subscription_name, topic_name):
    '''
    Shows ServiceBus Rule Details
    '''
    return call_az("az servicebus topic subscription rule show", locals())


def list(namespace_name, resource_group, subscription_name, topic_name, skip=None, top=None):
    '''
    List the ServiceBus Rule by Subscription
    '''
    return call_az("az servicebus topic subscription rule list", locals())


def delete(name, namespace_name, resource_group, subscription_name, topic_name):
    '''
    Deletes the ServiceBus Rule
    '''
    return call_az("az servicebus topic subscription rule delete", locals())


def update(name, namespace_name, resource_group, subscription_name, topic_name, action_compatibility_level=None, action_sql_expression=None, add=None, content_type=None, correlation_id=None, enable_action_preprocessing=None, enable_correlation_preprocessing=None, enable_sql_preprocessing=None, filter_sql_expression=None, force_string=None, label=None, message_id=None, remove=None, reply_to=None, reply_to_session_id=None, session_id=None, set=None, to=None):
    '''
    Updates the ServiceBus Rule for Subscription
    '''
    return call_az("az servicebus topic subscription rule update", locals())

