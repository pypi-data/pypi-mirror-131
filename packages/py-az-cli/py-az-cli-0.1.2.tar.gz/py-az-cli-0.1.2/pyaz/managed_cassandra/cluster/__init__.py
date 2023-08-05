from ... pyaz_utils import call_az

def create(cluster_name, delegated_management_subnet_id, location, resource_group, authentication_method=None, cassandra_version=None, client_certificates=None, cluster_name_override=None, external_gossip_certificates=None, external_seed_nodes=None, hours_between_backups=None, identity_type=None, initial_cassandra_admin_password=None, no_wait=None, repair_enabled=None, restore_from_backup_id=None, tags=None):
    '''
    Create a Managed Cassandra Cluster.
    '''
    return call_az("az managed-cassandra cluster create", locals())


def update(cluster_name, resource_group, authentication_method=None, cassandra_version=None, client_certificates=None, external_gossip_certificates=None, external_seed_nodes=None, hours_between_backups=None, identity_type=None, no_wait=None, repair_enabled=None, tags=None):
    '''
    Update a Managed Cassandra Cluster.
    '''
    return call_az("az managed-cassandra cluster update", locals())


def deallocate(cluster_name, resource_group, no_wait=None):
    '''
    Deallocate the Managed Cassandra Cluster and Associated Data Centers. Deallocation will deallocate the host virtual machine of this cluster, and reserved the data disk. This won't do anything on an already deallocated cluster. Use Start to restart the cluster.
    '''
    return call_az("az managed-cassandra cluster deallocate", locals())


def invoke_command(cluster_name, command_name, host, resource_group, arguments=None, cassandra_stop_start=None, no_wait=None, readwrite=None):
    '''
    Invoke a command like nodetool for cassandra maintenance.
    '''
    return call_az("az managed-cassandra cluster invoke-command", locals())


def start(cluster_name, resource_group, no_wait=None):
    '''
    Start the Managed Cassandra Cluster and Associated Data Centers. Start will start the host virtual machine of this cluster with reserved data disk. This won't do anything on an already running cluster. Use Deallocate to deallocate the cluster.
    '''
    return call_az("az managed-cassandra cluster start", locals())


def status(cluster_name, resource_group):
    '''
    Gets the CPU, memory, and disk usage statistics for each Cassandra node in a cluster.
    '''
    return call_az("az managed-cassandra cluster status", locals())


def list(resource_group=None):
    '''
    List the Managed Cassandra Clusters in a ResourceGroup and Subscription. If the ResourceGroup is not specified all the clusters in this Subscription are returned.
    '''
    return call_az("az managed-cassandra cluster list", locals())


def show(cluster_name, resource_group):
    '''
    Get a Managed Cassandra Cluster Resource.
    '''
    return call_az("az managed-cassandra cluster show", locals())


def delete(cluster_name, resource_group, no_wait=None, yes=None):
    '''
    Deletes a Managed Cassandra Cluster.
    '''
    return call_az("az managed-cassandra cluster delete", locals())

