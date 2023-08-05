from .... pyaz_utils import call_az

def list(application_name, gallery_name, resource_group):
    return call_az("az sig gallery-application version list", locals())


def show(application_name, gallery_name, name, resource_group, expand=None):
    return call_az("az sig gallery-application version show", locals())


def create(application_name, gallery_name, install_command, name, package_file_link, remove_command, resource_group, default_file_link=None, end_of_life_date=None, exclude_from=None, location=None, no_wait=None, tags=None, target_regions=None, update_command=None):
    '''
    Create a gallery Application Version.
    '''
    return call_az("az sig gallery-application version create", locals())


def update(application_name, gallery_name, name, package_file_link, resource_group, default_file_link=None, end_of_life_date=None, exclude_from=None, location=None, no_wait=None, tags=None, target_regions=None):
    '''
    Update a gallery Application Version.
    '''
    return call_az("az sig gallery-application version update", locals())


def delete(application_name, gallery_name, name, resource_group, no_wait=None, yes=None):
    return call_az("az sig gallery-application version delete", locals())

