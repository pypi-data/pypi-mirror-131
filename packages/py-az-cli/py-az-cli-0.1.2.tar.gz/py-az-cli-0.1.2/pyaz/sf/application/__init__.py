from ... pyaz_utils import call_az
from . import certificate


def list(cluster_name, resource_group):
    '''
    List applications of a given cluster.
    '''
    return call_az("az sf application list", locals())


def delete(cluster_name, name, resource_group):
    '''
    Delete an application.
    '''
    return call_az("az sf application delete", locals())


def show(cluster_name, name, resource_group):
    '''
    Show the properties of an application on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application show", locals())


def create(cluster_name, name, resource_group, type_name, version, max_nodes=None, min_nodes=None, package_url=None, parameters=None):
    '''
    Create a new application on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application create", locals())


def update(cluster_name, name, resource_group, failure_action=None, force_restart=None, hc_retry_timeout=None, hc_stable_duration=None, hc_wait_duration=None, max_nodes=None, max_porcent_unhealthy_apps=None, max_porcent_unhealthy_partitions=None, max_porcent_unhealthy_replicas=None, max_porcent_unhealthy_services=None, min_nodes=None, parameters=None, service_type_health_policy_map=None, ud_timeout=None, upgrade_replica_set_check_timeout=None, upgrade_timeout=None, version=None, warning_as_error=None):
    '''
    Update a Azure Service Fabric application. This allows updating the application parameters and/or upgrade the application type version which will trigger an application upgrade.
    '''
    return call_az("az sf application update", locals())

