from ... pyaz_utils import call_az

def create(gallery_image_definition, gallery_name, offer, os_type, publisher, resource_group, sku, description=None, disallowed_disk_types=None, end_of_life_date=None, eula=None, features=None, hyper_v_generation=None, location=None, maximum_cpu_core=None, maximum_memory=None, minimum_cpu_core=None, minimum_memory=None, os_state=None, plan_name=None, plan_product=None, plan_publisher=None, privacy_statement_uri=None, release_note_uri=None, tags=None):
    '''
    create a gallery image definition
    '''
    return call_az("az sig image-definition create", locals())


def list(gallery_name, resource_group):
    return call_az("az sig image-definition list", locals())


def show(gallery_image_definition, gallery_name, resource_group):
    return call_az("az sig image-definition show", locals())


def delete(gallery_image_definition, gallery_name, resource_group):
    return call_az("az sig image-definition delete", locals())


def update(gallery_image_definition, gallery_name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a VM Image definition.
    '''
    return call_az("az sig image-definition update", locals())


def list_shared(gallery_unique_name, location, shared_to=None):
    '''
    List VM Image definitions in a gallery shared directly to your subscription or tenant (preview).
    '''
    return call_az("az sig image-definition list-shared", locals())


def show_shared(gallery_image_definition, gallery_unique_name, location):
    '''
    Get a shared gallery image (preview).
    '''
    return call_az("az sig image-definition show-shared", locals())

