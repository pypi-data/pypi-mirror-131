from .... pyaz_utils import call_az

def list(name, resource_group):
    '''
    List all read replicas for a given server.
    '''
    return call_az("az mysql flexible-server replica list", locals())


def create(replica_name, resource_group, source_server, no_wait=None, zone=None):
    '''
    Create a read replica for a server.
    '''
    return call_az("az mysql flexible-server replica create", locals())


def stop_replication(name, resource_group, yes=None):
    '''
    Stop replication to a read replica and make it a read/write server.
    '''
    return call_az("az mysql flexible-server replica stop-replication", locals())

