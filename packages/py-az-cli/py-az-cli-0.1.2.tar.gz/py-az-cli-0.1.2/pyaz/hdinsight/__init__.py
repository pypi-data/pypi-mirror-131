from .. pyaz_utils import call_az
from . import application, autoscale, azure_monitor, host, monitor, script_action


def create(name, resource_group, type, assign_identity=None, autoscale_max_workernode_count=None, autoscale_min_workernode_count=None, autoscale_type=None, autoscale_workernode_count=None, cluster_admin_account=None, cluster_admin_password=None, cluster_configurations=None, cluster_tier=None, cluster_users_group_dns=None, component_version=None, days=None, domain=None, edgenode_size=None, enable_compute_isolation=None, enable_private_link=None, encryption_algorithm=None, encryption_at_host=None, encryption_in_transit=None, encryption_key_name=None, encryption_key_version=None, encryption_vault_uri=None, esp=None, headnode_size=None, host_sku=None, http_password=None, http_user=None, idbroker=None, kafka_client_group_id=None, kafka_client_group_name=None, kafka_management_node_count=None, kafka_management_node_size=None, ldaps_urls=None, location=None, minimal_tls_version=None, no_validation_timeout=None, no_wait=None, private_link_config=None, resource_provider_connection=None, ssh_password=None, ssh_public_key=None, ssh_user=None, storage_account=None, storage_account_key=None, storage_account_managed_identity=None, storage_container=None, storage_filesystem=None, subnet=None, tags=None, time=None, timezone=None, version=None, vnet_name=None, workernode_count=None, workernode_data_disk_size=None, workernode_data_disk_storage_account_type=None, workernode_data_disks_per_node=None, workernode_size=None, zones=None, zookeepernode_size=None):
    '''
    Create a new cluster.
    '''
    return call_az("az hdinsight create", locals())


def resize(name, resource_group, workernode_count, no_wait=None):
    '''
    Resize the specified HDInsight cluster to the specified size.
    '''
    return call_az("az hdinsight resize", locals())


def show(name, resource_group):
    return call_az("az hdinsight show", locals())


def list(resource_group=None):
    '''
    List HDInsight clusters in a resource group or subscription.
    '''
    return call_az("az hdinsight list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until an operation is complete.
    '''
    return call_az("az hdinsight wait", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    return call_az("az hdinsight delete", locals())


def rotate_disk_encryption_key(encryption_key_name, encryption_key_version, encryption_vault_uri, name, resource_group, no_wait=None):
    '''
    Rotate the disk encryption key of the specified HDInsight cluster.
    '''
    return call_az("az hdinsight rotate-disk-encryption-key", locals())


def update(name, resource_group, no_wait=None, tags=None):
    '''
    Update the tags of the specified HDInsight cluster.
    '''
    return call_az("az hdinsight update", locals())


def list_usage(location):
    return call_az("az hdinsight list-usage", locals())

