from .. pyaz_utils import call_az

def create(name, resource_group, accelerated_network=None, copy_start=None, disk_access=None, disk_encryption_set=None, edge_zone=None, encryption_type=None, for_upload=None, hyper_v_generation=None, incremental=None, location=None, network_access_policy=None, no_wait=None, public_network_access=None, size_gb=None, sku=None, source=None, source_storage_account_id=None, tags=None):
    '''
    Create a snapshot.
    '''
    return call_az("az snapshot create", locals())


def delete(name, resource_group):
    return call_az("az snapshot delete", locals())


def grant_access(duration_in_seconds, name, resource_group, access_level=None):
    '''
    Grant read access to a snapshot.
    '''
    return call_az("az snapshot grant-access", locals())


def list(resource_group=None):
    '''
    List snapshots.
    '''
    return call_az("az snapshot list", locals())


def revoke_access(name, resource_group):
    '''
    Revoke read access to a snapshot.
    '''
    return call_az("az snapshot revoke-access", locals())


def show(name, resource_group):
    return call_az("az snapshot show", locals())


def update(name, resource_group, accelerated_network=None, add=None, disk_access=None, disk_encryption_set=None, encryption_type=None, force_string=None, network_access_policy=None, no_wait=None, public_network_access=None, remove=None, set=None, sku=None):
    '''
    Update a snapshot.
    '''
    return call_az("az snapshot update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a snapshot is met.
    '''
    return call_az("az snapshot wait", locals())

