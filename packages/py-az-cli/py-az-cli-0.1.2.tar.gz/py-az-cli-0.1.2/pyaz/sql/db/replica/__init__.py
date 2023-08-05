from .... pyaz_utils import call_az

def create(name, partner_server, resource_group, server, auto_pause_delay=None, backup_storage_redundancy=None, capacity=None, compute_model=None, elastic_pool=None, family=None, license_type=None, min_capacity=None, no_wait=None, partner_database=None, partner_resource_group=None, read_replicas=None, read_scale=None, secondary_type=None, service_objective=None, tags=None, zone_redundant=None):
    '''
    Create a database as a readable secondary replica of an existing database.
    '''
    return call_az("az sql db replica create", locals())


def list_links(name, resource_group, server):
    '''
    List the replicas of a database and their replication status.
    '''
    return call_az("az sql db replica list-links", locals())


def delete_link(name, partner_server, resource_group, server, partner_resource_group=None, yes=None):
    '''
    Permanently stop data replication between two database replicas.
    '''
    return call_az("az sql db replica delete-link", locals())


def set_primary(name, resource_group, server, allow_data_loss=None):
    '''
    Set the primary replica database by failing over from the current primary replica database.
    '''
    return call_az("az sql db replica set-primary", locals())

