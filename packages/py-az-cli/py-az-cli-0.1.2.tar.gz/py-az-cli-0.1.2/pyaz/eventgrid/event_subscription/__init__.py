from ... pyaz_utils import call_az

def create(name, advanced_filter=None, azure_active_directory_application_id_or_uri=None, azure_active_directory_tenant_id=None, deadletter_endpoint=None, deadletter_identity=None, deadletter_identity_endpoint=None, delivery_attribute_mapping=None, delivery_identity=None, delivery_identity_endpoint=None, delivery_identity_endpoint_type=None, enable_advanced_filtering_on_arrays=None, endpoint=None, endpoint_type=None, event_delivery_schema=None, event_ttl=None, expiration_date=None, included_event_types=None, labels=None, max_delivery_attempts=None, max_events_per_batch=None, preferred_batch_size_in_kilobytes=None, source_resource_id=None, storage_queue_msg_ttl=None, subject_begins_with=None, subject_case_sensitive=None, subject_ends_with=None):
    '''
    Create a new event subscription.
    '''
    return call_az("az eventgrid event-subscription create", locals())


def show(name, include_full_endpoint_url=None, include_static_delivery_attribute_secret=None, source_resource_id=None):
    '''
    Get the details of an event subscription.
    '''
    return call_az("az eventgrid event-subscription show", locals())


def delete(name, source_resource_id=None):
    '''
    Delete an event subscription.
    '''
    return call_az("az eventgrid event-subscription delete", locals())


def list(location=None, odata_query=None, resource_group=None, source_resource_id=None, topic_type_name=None):
    '''
    List event subscriptions.
    '''
    return call_az("az eventgrid event-subscription list", locals())


def update(name, add=None, advanced_filter=None, deadletter_endpoint=None, deadletter_identity=None, deadletter_identity_endpoint=None, delivery_attribute_mapping=None, delivery_identity=None, delivery_identity_endpoint=None, delivery_identity_endpoint_type=None, enable_advanced_filtering_on_arrays=None, endpoint=None, endpoint_type=None, force_string=None, included_event_types=None, labels=None, remove=None, set=None, source_resource_id=None, storage_queue_msg_ttl=None, subject_begins_with=None, subject_ends_with=None):
    '''
    Update an event subscription.
    '''
    return call_az("az eventgrid event-subscription update", locals())

