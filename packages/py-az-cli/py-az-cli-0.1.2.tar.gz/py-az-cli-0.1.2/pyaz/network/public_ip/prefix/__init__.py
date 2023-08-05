from .... pyaz_utils import call_az

def create(length, name, resource_group, custom_ip_prefix_name=None, edge_zone=None, location=None, tags=None, version=None, zone=None):
    '''
    Create a public IP prefix resource.
    '''
    return call_az("az network public-ip prefix create", locals())


def delete(name, resource_group):
    '''
    Delete a public IP prefix resource.
    '''
    return call_az("az network public-ip prefix delete", locals())


def list(resource_group=None):
    '''
    List public IP prefix resources.
    '''
    return call_az("az network public-ip prefix list", locals())


def show(name, resource_group, expand=None):
    '''
    Get the details of a public IP prefix resource.
    '''
    return call_az("az network public-ip prefix show", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update a public IP prefix resource.
    '''
    return call_az("az network public-ip prefix update", locals())

