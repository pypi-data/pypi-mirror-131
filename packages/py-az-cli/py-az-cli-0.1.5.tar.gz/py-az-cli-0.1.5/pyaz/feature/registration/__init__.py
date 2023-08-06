from ... pyaz_utils import _call_az

def list(namespace=None):
    '''
    List feature registrations.
    '''
    return _call_az("az feature registration list", locals())


def show(name, provider_namespace):
    return _call_az("az feature registration show", locals())


def create(name, namespace):
    '''
    Create a feature registration.
    '''
    return _call_az("az feature registration create", locals())


def delete(name, namespace, yes=None):
    '''
    Delete a feature registration.
    '''
    return _call_az("az feature registration delete", locals())

