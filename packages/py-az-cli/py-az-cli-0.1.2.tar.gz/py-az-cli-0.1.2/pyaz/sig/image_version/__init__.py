from ... pyaz_utils import call_az

def delete(gallery_image_definition, gallery_image_version, gallery_name, resource_group):
    return call_az("az sig image-version delete", locals())


def show(gallery_image_definition, gallery_image_version, gallery_name, resource_group, expand=None):
    return call_az("az sig image-version show", locals())


def list(gallery_image_definition, gallery_name, resource_group):
    return call_az("az sig image-version list", locals())


def create(gallery_image_definition, gallery_image_version, gallery_name, resource_group, data_snapshot_luns=None, data_snapshots=None, data_vhds_luns=None, data_vhds_storage_accounts=None, data_vhds_uris=None, end_of_life_date=None, exclude_from_latest=None, location=None, managed_image=None, no_wait=None, os_snapshot=None, os_vhd_storage_account=None, os_vhd_uri=None, replica_count=None, replication_mode=None, storage_account_type=None, tags=None, target_region_encryption=None, target_regions=None):
    '''
    create a new image version
    '''
    return call_az("az sig image-version create", locals())


def update(gallery_image_definition, gallery_image_version, gallery_name, resource_group, add=None, force_string=None, no_wait=None, remove=None, replica_count=None, set=None, target_regions=None):
    '''
    update a share image version
    '''
    return call_az("az sig image-version update", locals())


def wait(gallery_image_definition, gallery_image_version, gallery_name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    wait for image version related operation
    '''
    return call_az("az sig image-version wait", locals())


def list_shared(gallery_image_definition, gallery_unique_name, location, shared_to=None):
    '''
    List VM Image Versions in a gallery shared directly to your subscription or tenant (preview).
    '''
    return call_az("az sig image-version list-shared", locals())


def show_shared(gallery_image_definition, gallery_image_version, gallery_unique_name, location):
    '''
    Get an image version in a gallery shared directly to your subscription or tenant (preview).
    '''
    return call_az("az sig image-version show-shared", locals())

