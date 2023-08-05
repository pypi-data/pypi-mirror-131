from ... pyaz_utils import call_az

def list(cluster_name, resource_group):
    '''
    List managed applications of a given managed cluster.
    '''
    return call_az("az sf managed-application list", locals())


def delete(cluster_name, name, resource_group):
    '''
    Delete a managed application.
    '''
    return call_az("az sf managed-application delete", locals())


def show(cluster_name, name, resource_group):
    '''
    Show the properties of a managed application on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application show", locals())


def create(cluster_name, name, resource_group, type_name, version, package_url=None, parameters=None, tags=None):
    '''
    Create a new managed application on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application create", locals())


def update(cluster_name, name, resource_group, failure_action=None, force_restart=None, hc_retry_timeout=None, hc_stable_duration=None, hc_wait_duration=None, instance_close_delay_duration=None, max_percent_unhealthy_deployed_applications=None, max_percent_unhealthy_partitions=None, max_percent_unhealthy_replicas=None, max_percent_unhealthy_services=None, parameters=None, recreate_application=None, service_type_health_policy_map=None, tags=None, ud_timeout=None, upgrade_mode=None, upgrade_replica_set_check_timeout=None, upgrade_timeout=None, version=None, warning_as_error=None):
    '''
    Update a Azure Service Fabric managed application.
    '''
    return call_az("az sf managed-application update", locals())

