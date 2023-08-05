from .. pyaz_utils import call_az
from . import gallery_application, image_definition, image_version, share


def create(gallery_name, resource_group, description=None, location=None, permissions=None, soft_delete=None, tags=None):
    '''
    Create a shared image gallery.
    '''
    return call_az("az sig create", locals())


def show(gallery_name, resource_group, select=None):
    return call_az("az sig show", locals())


def list(resource_group=None):
    '''
    list share image galleries.
    '''
    return call_az("az sig list", locals())


def delete(gallery_name, resource_group):
    return call_az("az sig delete", locals())


def update(gallery_name, resource_group, add=None, force_string=None, permissions=None, remove=None, select=None, set=None, soft_delete=None):
    '''
    update a share image gallery.
    '''
    return call_az("az sig update", locals())


def list_shared(location, shared_to=None):
    '''
    List all galleries shared directly to your subscription or tenant (preview).
    '''
    return call_az("az sig list-shared", locals())


def show_shared(gallery_unique_name, location):
    '''
    Get a gallery that has been shared directly to your subscription or tenant (preview).
    '''
    return call_az("az sig show-shared", locals())

