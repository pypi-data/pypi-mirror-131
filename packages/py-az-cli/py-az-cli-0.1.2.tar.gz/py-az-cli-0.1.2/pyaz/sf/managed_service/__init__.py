from ... pyaz_utils import call_az
from . import correlation_scheme, load_metrics


def list(application, cluster_name, resource_group):
    '''
    List managed services of a given managed application.
    '''
    return call_az("az sf managed-service list", locals())


def delete(application, cluster_name, name, resource_group):
    '''
    Delete a managed service.
    '''
    return call_az("az sf managed-service delete", locals())


def show(application, cluster_name, name, resource_group):
    '''
    Get a service.
    '''
    return call_az("az sf managed-service show", locals())


def create(application, cluster_name, name, resource_group, state, type, default_move_cost=None, has_persisted_state=None, high_key=None, instance_count=None, low_key=None, min_instance_count=None, min_instance_percentage=None, min_replica_set_size=None, partition_count=None, partition_names=None, partition_scheme=None, placement_constraints=None, quorum_loss_wait_duration=None, replica_restart_wait_duration=None, service_package_activation_mode=None, service_placement_time_limit=None, stand_by_replica_keep_duration=None, tags=None, target_replica_set_size=None):
    '''
    Create a new managed service on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-service create", locals())


def update(application, cluster_name, name, resource_group, default_move_cost=None, instance_count=None, min_instance_count=None, min_instance_percentage=None, min_replica_set_size=None, placement_constraints=None, quorum_loss_wait_duration=None, replica_restart_wait_duration=None, service_placement_time_limit=None, stand_by_replica_keep_duration=None, tags=None, target_replica_set_size=None):
    '''
    Update a managed service.
    '''
    return call_az("az sf managed-service update", locals())

