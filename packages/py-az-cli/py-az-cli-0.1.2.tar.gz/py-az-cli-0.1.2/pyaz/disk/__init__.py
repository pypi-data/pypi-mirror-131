from .. pyaz_utils import call_az

def create(name, resource_group, accelerated_network=None, disk_access=None, disk_encryption_set=None, disk_iops_read_only=None, disk_iops_read_write=None, disk_mbps_read_only=None, disk_mbps_read_write=None, edge_zone=None, enable_bursting=None, encryption_type=None, for_upload=None, gallery_image_reference=None, gallery_image_reference_lun=None, hyper_v_generation=None, image_reference=None, image_reference_lun=None, location=None, logical_sector_size=None, max_shares=None, network_access_policy=None, no_wait=None, os_type=None, public_network_access=None, security_type=None, size_gb=None, sku=None, source=None, source_storage_account_id=None, support_hibernation=None, tags=None, tier=None, upload_size_bytes=None, zone=None):
    '''
    Create a managed disk.
    '''
    return call_az("az disk create", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a managed disk.
    '''
    return call_az("az disk delete", locals())


def grant_access(duration_in_seconds, name, resource_group, access_level=None):
    '''
    Grant a resource access to a managed disk.
    '''
    return call_az("az disk grant-access", locals())


def list(resource_group=None):
    '''
    List managed disks.
    '''
    return call_az("az disk list", locals())


def revoke_access(name, resource_group):
    '''
    Revoke a resource's read access to a managed disk.
    '''
    return call_az("az disk revoke-access", locals())


def show(name, resource_group):
    return call_az("az disk show", locals())


def update(name, resource_group, accelerated_network=None, add=None, disk_access=None, disk_encryption_set=None, disk_iops_read_only=None, disk_iops_read_write=None, disk_mbps_read_only=None, disk_mbps_read_write=None, enable_bursting=None, encryption_type=None, force_string=None, max_shares=None, network_access_policy=None, no_wait=None, public_network_access=None, remove=None, set=None, size_gb=None, sku=None):
    '''
    Update a managed disk.
    '''
    return call_az("az disk update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a managed disk is met.
    '''
    return call_az("az disk wait", locals())

