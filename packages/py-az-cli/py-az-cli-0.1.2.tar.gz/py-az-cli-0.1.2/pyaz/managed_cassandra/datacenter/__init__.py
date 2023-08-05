from ... pyaz_utils import call_az

def create(cluster_name, data_center_location, data_center_name, delegated_subnet_id, node_count, resource_group, availability_zone=None, backup_storage_customer_key_uri=None, base64_encoded_cassandra_yaml_fragment=None, disk_capacity=None, disk_sku=None, managed_disk_customer_key_uri=None, no_wait=None, sku=None):
    '''
    Create a Datacenter in an Azure Managed Cassandra Cluster.
    '''
    return call_az("az managed-cassandra datacenter create", locals())


def update(cluster_name, data_center_name, resource_group, backup_storage_customer_key_uri=None, base64_encoded_cassandra_yaml_fragment=None, managed_disk_customer_key_uri=None, no_wait=None, node_count=None):
    '''
    Update a Datacenter in an Azure Managed Cassandra Cluster.
    '''
    return call_az("az managed-cassandra datacenter update", locals())


def list(cluster_name, resource_group):
    '''
    List the Managed Cassandra Datacenters in a given Cluster.
    '''
    return call_az("az managed-cassandra datacenter list", locals())


def show(cluster_name, data_center_name, resource_group):
    '''
    Get a Managed Cassandra DataCenter Resource.
    '''
    return call_az("az managed-cassandra datacenter show", locals())


def delete(cluster_name, data_center_name, resource_group, no_wait=None, yes=None):
    '''
    Deletes a Managed Cassandra Datacenter.
    '''
    return call_az("az managed-cassandra datacenter delete", locals())

