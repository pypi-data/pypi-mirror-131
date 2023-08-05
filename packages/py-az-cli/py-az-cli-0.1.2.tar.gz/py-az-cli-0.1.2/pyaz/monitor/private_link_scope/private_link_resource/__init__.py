from .... pyaz_utils import call_az

def show(name, resource_group, scope_name):
    '''
    Show a private link resource of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-link-resource show", locals())


def list(resource_group, scope_name):
    '''
    List all private link resources of a private link scope resource.
    '''
    return call_az("az monitor private-link-scope private-link-resource list", locals())

