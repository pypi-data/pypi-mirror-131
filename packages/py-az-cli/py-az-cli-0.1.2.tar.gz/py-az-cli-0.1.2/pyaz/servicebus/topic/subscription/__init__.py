from .... pyaz_utils import call_az
from . import rule


def create(name, namespace_name, resource_group, topic_name, auto_delete_on_idle=None, dead_letter_on_filter_exceptions=None, default_message_time_to_live=None, enable_batched_operations=None, enable_dead_lettering_on_message_expiration=None, enable_session=None, forward_dead_lettered_messages_to=None, forward_to=None, lock_duration=None, max_delivery_count=None, status=None):
    '''
    Create the ServiceBus Subscription
    '''
    return call_az("az servicebus topic subscription create", locals())


def show(name, namespace_name, resource_group, topic_name):
    '''
    Shows Service Bus Subscription Details
    '''
    return call_az("az servicebus topic subscription show", locals())


def list(namespace_name, resource_group, topic_name, skip=None, top=None):
    '''
    List the Subscription by Service Bus Topic
    '''
    return call_az("az servicebus topic subscription list", locals())


def delete(name, namespace_name, resource_group, topic_name):
    '''
    Deletes the Service Bus Subscription
    '''
    return call_az("az servicebus topic subscription delete", locals())


def update(name, namespace_name, resource_group, topic_name, add=None, auto_delete_on_idle=None, dead_letter_on_filter_exceptions=None, default_message_time_to_live=None, enable_batched_operations=None, enable_dead_lettering_on_message_expiration=None, enable_session=None, force_string=None, forward_dead_lettered_messages_to=None, forward_to=None, lock_duration=None, max_delivery_count=None, remove=None, set=None, status=None):
    '''
    Updates the ServiceBus Subscription
    '''
    return call_az("az servicebus topic subscription update", locals())

