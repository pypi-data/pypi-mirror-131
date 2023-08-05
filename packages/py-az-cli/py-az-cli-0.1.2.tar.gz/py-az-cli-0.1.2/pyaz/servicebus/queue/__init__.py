from ... pyaz_utils import call_az
from . import authorization_rule


def create(name, namespace_name, resource_group, auto_delete_on_idle=None, default_message_time_to_live=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_dead_lettering_on_message_expiration=None, enable_duplicate_detection=None, enable_express=None, enable_partitioning=None, enable_session=None, forward_dead_lettered_messages_to=None, forward_to=None, lock_duration=None, max_delivery_count=None, max_size=None, status=None):
    '''
    Create the Service Bus Queue
    '''
    return call_az("az servicebus queue create", locals())


def show(name, namespace_name, resource_group):
    '''
    shows the Service Bus Queue Details
    '''
    return call_az("az servicebus queue show", locals())


def list(namespace_name, resource_group, skip=None, top=None):
    '''
    List the Queue by Service Bus Namespace
    '''
    return call_az("az servicebus queue list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Service Bus Queue
    '''
    return call_az("az servicebus queue delete", locals())


def update(name, namespace_name, resource_group, add=None, auto_delete_on_idle=None, default_message_time_to_live=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_dead_lettering_on_message_expiration=None, enable_duplicate_detection=None, enable_express=None, enable_partitioning=None, enable_session=None, force_string=None, forward_dead_lettered_messages_to=None, forward_to=None, lock_duration=None, max_delivery_count=None, max_size=None, remove=None, set=None, status=None):
    '''
    Updates existing Service Bus Queue
    '''
    return call_az("az servicebus queue update", locals())

