from .... pyaz_utils import call_az

def add(name, resource_group, artifact_tags=None, gallery_image_definition=None, gallery_name=None, gallery_replication_regions=None, is_vhd=None, managed_image=None, managed_image_location=None, output_name=None):
    '''
    Add an image builder output distributor to an image builder template.
    '''
    return call_az("az image builder output add", locals())


def remove(name, output_name, resource_group):
    '''
    Remove an image builder output distributor from an image builder template.
    '''
    return call_az("az image builder output remove", locals())


def clear(name, resource_group):
    '''
    Remove all image builder output distributors from an image builder template.
    '''
    return call_az("az image builder output clear", locals())

