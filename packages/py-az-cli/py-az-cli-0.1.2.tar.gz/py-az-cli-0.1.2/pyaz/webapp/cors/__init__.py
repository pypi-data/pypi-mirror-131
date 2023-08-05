from ... pyaz_utils import call_az

def add(allowed_origins, name, resource_group, slot=None):
    '''
    Add allowed origins
    '''
    return call_az("az webapp cors add", locals())


def remove(allowed_origins, name, resource_group, slot=None):
    '''
    Remove allowed origins
    '''
    return call_az("az webapp cors remove", locals())


def show(name, resource_group, slot=None):
    '''
    show allowed origins
    '''
    return call_az("az webapp cors show", locals())

