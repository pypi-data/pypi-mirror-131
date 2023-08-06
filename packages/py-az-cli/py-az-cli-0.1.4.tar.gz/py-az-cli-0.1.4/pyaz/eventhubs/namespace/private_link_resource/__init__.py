from .... pyaz_utils import _call_az

def show(namespace_name, resource_group):
    '''
    Get the private link resources that need to be created for a eventhubs namespace.
    '''
    return _call_az("az eventhubs namespace private-link-resource show", locals())

