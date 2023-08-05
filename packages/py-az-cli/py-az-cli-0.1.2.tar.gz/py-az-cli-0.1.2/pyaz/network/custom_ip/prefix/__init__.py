from .... pyaz_utils import call_az

def create(name, resource_group, authorization_message=None, cidr=None, cip_prefix_parent=None, location=None, no_wait=None, signed_message=None, tags=None, zone=None):
    '''
    Create a custom IP prefix resource.
    '''
    return call_az("az network custom-ip prefix create", locals())


def delete(name, resource_group):
    '''
    Delete a custom IP prefix resource.
    '''
    return call_az("az network custom-ip prefix delete", locals())


def list(resource_group=None):
    '''
    List custom IP prefix resources.
    '''
    return call_az("az network custom-ip prefix list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a custom IP prefix resource.
    '''
    return call_az("az network custom-ip prefix show", locals())


def update(name, resource_group, add=None, authorization_message=None, force_string=None, no_wait=None, remove=None, set=None, signed_message=None, state=None, tags=None):
    '''
    Update a custom IP prefix resource.
    '''
    return call_az("az network custom-ip prefix update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, expand=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the custom ip prefix is met.
    '''
    return call_az("az network custom-ip prefix wait", locals())

