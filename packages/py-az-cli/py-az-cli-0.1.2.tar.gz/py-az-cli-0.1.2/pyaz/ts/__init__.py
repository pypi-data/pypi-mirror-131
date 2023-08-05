from .. pyaz_utils import call_az

def create(name, resource_group, description=None, display_name=None, location=None, tags=None, template_file=None, ui_form_definition=None, version=None, version_description=None, yes=None):
    '''
    Create a template spec and or template spec version.
    '''
    return call_az("az ts create", locals())


def update(description=None, display_name=None, name=None, resource_group=None, tags=None, template_file=None, template_spec=None, ui_form_definition=None, version=None, version_description=None, yes=None):
    '''
    Update a template spec version.
    '''
    return call_az("az ts update", locals())


def export(output_folder, name=None, resource_group=None, template_spec=None, version=None):
    '''
    Export the specified template spec version and artifacts (if any) to the specified output folder.
    '''
    return call_az("az ts export", locals())


def show(name=None, resource_group=None, template_spec=None, version=None):
    '''
    Get the specified template spec or template spec version.
    '''
    return call_az("az ts show", locals())


def list(name=None, resource_group=None):
    '''
    List template specs or template spec versions.
    '''
    return call_az("az ts list", locals())


def delete(name=None, resource_group=None, template_spec=None, version=None, yes=None):
    '''
    Delete a specified template spec or template spec version by name or resource ID..
    '''
    return call_az("az ts delete", locals())

