from ... pyaz_utils import call_az

def assign(name, identities=None, resource_group=None):
    '''
    Update managed identities for an App Configuration.
    '''
    return call_az("az appconfig identity assign", locals())


def remove(name, identities=None, resource_group=None):
    '''
    Remove managed identities for an App Configuration.
    '''
    return call_az("az appconfig identity remove", locals())


def show(name, resource_group=None):
    '''
    Display managed identities for an App Configuration.
    '''
    return call_az("az appconfig identity show", locals())

