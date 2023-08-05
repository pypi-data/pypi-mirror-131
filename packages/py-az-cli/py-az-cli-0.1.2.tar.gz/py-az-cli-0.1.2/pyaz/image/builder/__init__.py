from ... pyaz_utils import call_az
from . import customizer, output


def create(name, resource_group, build_timeout=None, checksum=None, identity=None, image_source=None, image_template=None, location=None, managed_image_destinations=None, no_wait=None, os_disk_size=None, scripts=None, shared_image_destinations=None, subnet=None, tags=None, vm_size=None, vnet=None):
    '''
    Create an image builder template.
    '''
    return call_az("az image builder create", locals())


def list(resource_group=None):
    '''
    List image builder templates.
    '''
    return call_az("az image builder list", locals())


def show(name, resource_group):
    '''
    Show an image builder template.
    '''
    return call_az("az image builder show", locals())


def delete(name, resource_group):
    '''
    Delete image builder template.
    '''
    return call_az("az image builder delete", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update an image builder template.
    '''
    return call_az("az image builder update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the template is met.
    '''
    return call_az("az image builder wait", locals())


def run(name, resource_group, no_wait=None):
    '''
    Build an image builder template.
    '''
    return call_az("az image builder run", locals())


def show_runs(name, resource_group, output_name=None):
    '''
    Show an image builder template's run outputs.
    '''
    return call_az("az image builder show-runs", locals())


def cancel(name, resource_group):
    '''
    Cancel the long running image build based on the image template.
    '''
    return call_az("az image builder cancel", locals())

