from .... pyaz_utils import call_az

def show(name, resource_group, scope_name):
    '''
    Show a scoped resource of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope scoped-resource show", locals())


def list(resource_group, scope_name):
    '''
    List all scoped resource of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope scoped-resource list", locals())


def create(linked_resource, name, resource_group, scope_name):
    '''
    Create a scoped resource for a private link scope resource.
    '''
    return call_az("az monitor private-link-scope scoped-resource create", locals())


def delete(name, resource_group, scope_name, yes=None):
    '''
    Delete a scoped resource of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope scoped-resource delete", locals())

