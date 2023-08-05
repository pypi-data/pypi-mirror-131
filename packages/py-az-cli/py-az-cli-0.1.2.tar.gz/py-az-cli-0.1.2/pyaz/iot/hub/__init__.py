from ... pyaz_utils import call_az
from . import certificate, consumer_group, devicestream, identity, message_enrichment, policy, route, routing_endpoint


def create(name, resource_group, c2d_max_delivery_count=None, c2d_ttl=None, disable_device_sas=None, disable_local_auth=None, disable_module_sas=None, feedback_lock_duration=None, feedback_max_delivery_count=None, feedback_ttl=None, fileupload_notification_lock_duration=None, fileupload_notification_max_delivery_count=None, fileupload_notification_ttl=None, fileupload_notifications=None, fileupload_sas_ttl=None, fileupload_storage_auth_type=None, fileupload_storage_connectionstring=None, fileupload_storage_container_name=None, fileupload_storage_container_uri=None, fileupload_storage_identity=None, location=None, mi_system_assigned=None, mi_user_assigned=None, min_tls_version=None, partition_count=None, retention_day=None, role=None, scopes=None, sku=None, tags=None, unit=None):
    '''
    Create an Azure IoT hub.
    '''
    return call_az("az iot hub create", locals())


def list(resource_group=None):
    '''
    List IoT hubs.
    '''
    return call_az("az iot hub list", locals())


def show_connection_string(all=None, hub_name=None, key=None, policy_name=None, resource_group=None):
    '''
    Show the connection strings for an IoT hub.
    '''
    return call_az("az iot hub show-connection-string", locals())


def show(name, resource_group=None):
    '''
    Get the details of an IoT hub.
    '''
    return call_az("az iot hub show", locals())


def update(name, add=None, c2d_max_delivery_count=None, c2d_ttl=None, disable_device_sas=None, disable_local_auth=None, disable_module_sas=None, feedback_lock_duration=None, feedback_max_delivery_count=None, feedback_ttl=None, fileupload_notification_lock_duration=None, fileupload_notification_max_delivery_count=None, fileupload_notification_ttl=None, fileupload_notifications=None, fileupload_sas_ttl=None, fileupload_storage_auth_type=None, fileupload_storage_connectionstring=None, fileupload_storage_container_name=None, fileupload_storage_container_uri=None, fileupload_storage_identity=None, force_string=None, remove=None, resource_group=None, retention_day=None, set=None, sku=None, tags=None, unit=None):
    '''
    Update metadata for an IoT hub.
    '''
    return call_az("az iot hub update", locals())


def delete(name, resource_group=None):
    '''
    Delete an IoT hub.
    '''
    return call_az("az iot hub delete", locals())


def list_skus(name, resource_group=None):
    '''
    List available pricing tiers.
    '''
    return call_az("az iot hub list-skus", locals())


def show_quota_metrics(name, resource_group=None):
    '''
    Get the quota metrics for an IoT hub.
    '''
    return call_az("az iot hub show-quota-metrics", locals())


def show_stats(name, resource_group=None):
    '''
    Get the statistics for an IoT hub.
    '''
    return call_az("az iot hub show-stats", locals())


def manual_failover(name, no_wait=None, resource_group=None):
    '''
    Initiate a manual failover for the IoT Hub to the geo-paired disaster recovery region.
    '''
    return call_az("az iot hub manual-failover", locals())

