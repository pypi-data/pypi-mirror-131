from ... pyaz_utils import call_az

def list(application_name, cluster_name, resource_group):
    '''
    List services of a given application.
    '''
    return call_az("az sf service list", locals())


def delete(application_name, cluster_name, name, resource_group):
    '''
    Delete a service.
    '''
    return call_az("az sf service delete", locals())


def show(application_name, cluster_name, name, resource_group):
    '''
    Get a service.
    '''
    return call_az("az sf service show", locals())


def create(application, cluster_name, name, resource_group, service_type, state, default_move_cost=None, instance_count=None, min_replica_set_size=None, partition_scheme=None, target_replica_set_size=None):
    '''
    Create a new service on an Azure Service Fabric cluster.
    '''
    return call_az("az sf service create", locals())

