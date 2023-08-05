from ... pyaz_utils import call_az
from . import authorization_rule, network_rule, private_endpoint_connection, private_link_resource


def create(name, resource_group, assign_identity=None, capacity=None, cluster_arm_id=None, default_action=None, disable_local_auth=None, enable_auto_inflate=None, enable_kafka=None, enable_trusted_service_access=None, location=None, maximum_throughput_units=None, sku=None, tags=None, zone_redundant=None):
    '''
    Creates the EventHubs Namespace
    '''
    return call_az("az eventhubs namespace create", locals())


def show(name, resource_group):
    '''
    shows the Event Hubs Namespace Details
    '''
    return call_az("az eventhubs namespace show", locals())


def list(resource_group=None):
    '''
    Lists the EventHubs Namespaces
    '''
    return call_az("az eventhubs namespace list", locals())


def delete(name, resource_group):
    '''
    Deletes the Namespaces
    '''
    return call_az("az eventhubs namespace delete", locals())


def exists(name):
    '''
    check for the availability of the given name for the Namespace
    '''
    return call_az("az eventhubs namespace exists", locals())


def update(name, resource_group, add=None, assign_identity=None, capacity=None, default_action=None, disable_local_auth=None, enable_auto_inflate=None, enable_kafka=None, enable_trusted_service_access=None, force_string=None, infra_encryption=None, key_name=None, key_source=None, key_vault_uri=None, key_version=None, maximum_throughput_units=None, remove=None, set=None, sku=None, tags=None):
    '''
    Updates the EventHubs Namespace
    '''
    return call_az("az eventhubs namespace update", locals())

