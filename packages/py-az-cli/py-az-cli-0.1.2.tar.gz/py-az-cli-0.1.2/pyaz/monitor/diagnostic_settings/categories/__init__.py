from .... pyaz_utils import call_az

def show(name, resource, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    return call_az("az monitor diagnostic-settings categories show", locals())


def list(resource, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    '''
    List the diagnostic settings categories for the specified resource.
    '''
    return call_az("az monitor diagnostic-settings categories list", locals())

