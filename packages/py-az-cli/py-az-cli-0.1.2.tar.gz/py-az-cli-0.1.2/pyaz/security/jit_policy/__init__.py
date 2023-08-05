from ... pyaz_utils import call_az

def list(location=None, resource_group=None):
    '''
    List your Just in Time network access policies.
    '''
    return call_az("az security jit-policy list", locals())


def show(location, name, resource_group):
    '''
    Shows a Just in Time network access policy.
    '''
    return call_az("az security jit-policy show", locals())

