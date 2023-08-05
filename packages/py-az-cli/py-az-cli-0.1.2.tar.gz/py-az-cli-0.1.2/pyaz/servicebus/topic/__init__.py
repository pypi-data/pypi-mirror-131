from ... pyaz_utils import call_az
from . import authorization_rule, subscription


def create(name, namespace_name, resource_group, auto_delete_on_idle=None, default_message_time_to_live=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_duplicate_detection=None, enable_express=None, enable_ordering=None, enable_partitioning=None, max_size=None, status=None):
    '''
    Create the Service Bus Topic
    '''
    return call_az("az servicebus topic create", locals())


def show(name, namespace_name, resource_group):
    '''
    Shows the Service Bus Topic Details
    '''
    return call_az("az servicebus topic show", locals())


def list(namespace_name, resource_group, skip=None, top=None):
    '''
    List the Topic by Service Bus Namespace
    '''
    return call_az("az servicebus topic list", locals())


def delete(name, namespace_name, resource_group):
    '''
    Deletes the Service Bus Topic
    '''
    return call_az("az servicebus topic delete", locals())


def update(name, namespace_name, resource_group, add=None, auto_delete_on_idle=None, default_message_time_to_live=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_duplicate_detection=None, enable_express=None, enable_ordering=None, enable_partitioning=None, force_string=None, max_size=None, remove=None, set=None, status=None):
    '''
    Updates the Service Bus Topic
    '''
    return call_az("az servicebus topic update", locals())

