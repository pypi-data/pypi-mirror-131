from ... pyaz_utils import _call_az

def assign(name, resource_group, identities=None, role=None, scope=None, slot=None):
    '''
    assign managed identity to the web app
    '''
    return _call_az("az functionapp identity assign", locals())


def show(name, resource_group, slot=None):
    '''
    display web app's managed identity
    '''
    return _call_az("az functionapp identity show", locals())


def remove(name, resource_group, identities=None, slot=None):
    '''
    Disable web app's managed identity
    '''
    return _call_az("az functionapp identity remove", locals())

