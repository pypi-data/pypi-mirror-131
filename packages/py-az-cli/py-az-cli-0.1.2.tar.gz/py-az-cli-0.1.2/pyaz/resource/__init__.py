from .. pyaz_utils import call_az
from . import link, lock


def create(properties, api_version=None, id=None, is_full_object=None, latest_include_preview=None, location=None, name=None, namespace=None, parent=None, resource_group=None, resource_type=None):
    '''
    create a resource.
    '''
    return call_az("az resource create", locals())


def delete(api_version=None, ids=None, latest_include_preview=None, name=None, namespace=None, parent=None, resource_group=None, resource_type=None):
    '''
    Delete a resource.
    '''
    return call_az("az resource delete", locals())


def show(api_version=None, ids=None, include_response_body=None, latest_include_preview=None, name=None, namespace=None, parent=None, resource_group=None, resource_type=None):
    '''
    Get the details of a resource.
    '''
    return call_az("az resource show", locals())


def list(location=None, name=None, namespace=None, resource_group=None, resource_type=None, tag=None):
    '''
    List resources.
    '''
    return call_az("az resource list", locals())


def tag(tags, api_version=None, ids=None, is_incremental=None, latest_include_preview=None, name=None, namespace=None, parent=None, resource_group=None, resource_type=None):
    '''
    Tag a resource.
    '''
    return call_az("az resource tag", locals())


def move(destination_group, ids, destination_subscription_id=None):
    return call_az("az resource move", locals())


def invoke_action(action, api_version=None, ids=None, latest_include_preview=None, name=None, namespace=None, parent=None, request_body=None, resource_group=None, resource_type=None):
    '''
    Invoke an action on the resource.
    '''
    return call_az("az resource invoke-action", locals())


def update(add=None, api_version=None, force_string=None, ids=None, include_response_body=None, latest_include_preview=None, name=None, namespace=None, parent=None, remove=None, resource_group=None, resource_type=None, set=None):
    '''
    Update a resource.
    '''
    return call_az("az resource update", locals())


def wait(api_version=None, created=None, custom=None, deleted=None, exists=None, ids=None, include_response_body=None, interval=None, name=None, namespace=None, parent=None, resource_group=None, resource_type=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a resources is met.
    '''
    return call_az("az resource wait", locals())

