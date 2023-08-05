from .... pyaz_utils import call_az

def show(id=None, name=None, resource_group=None, scope_name=None):
    '''
    Show a private endpoint connection of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-endpoint-connection show", locals())


def list(resource_group, scope_name):
    '''
    List all private endpoint connections of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-endpoint-connection list", locals())


def approve(description=None, id=None, name=None, resource_group=None, scope_name=None):
    '''
    Approve a private endpoint connection of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-endpoint-connection approve", locals())


def reject(description=None, id=None, name=None, resource_group=None, scope_name=None):
    '''
    Reject a private endpoint connection of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-endpoint-connection reject", locals())


def delete(id=None, name=None, resource_group=None, scope_name=None, yes=None):
    '''
    Delete a private endpoint connection of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-endpoint-connection delete", locals())

