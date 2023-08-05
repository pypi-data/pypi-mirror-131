from ..... pyaz_utils import call_az

def list(gateway_name, resource_group):
    '''
    List rewrite rule sets.
    '''
    return call_az("az network application-gateway rewrite-rule set list", locals())


def show(gateway_name, name, resource_group):
    '''
    Get the details of a rewrite rule set.
    '''
    return call_az("az network application-gateway rewrite-rule set show", locals())


def delete(gateway_name, name, resource_group, no_wait=None):
    '''
    Delete a rewrite rule set.
    '''
    return call_az("az network application-gateway rewrite-rule set delete", locals())


def create(gateway_name, name, resource_group, no_wait=None):
    '''
    Create a rewrite rule set.
    '''
    return call_az("az network application-gateway rewrite-rule set create", locals())


def update(gateway_name, name, resource_group, add=None, force_string=None, no_wait=None, remove=None, set=None):
    '''
    Update a rewrite rule set.
    '''
    return call_az("az network application-gateway rewrite-rule set update", locals())

