from .. pyaz_utils import call_az
from . import registration


def list(namespace=None):
    '''
    List preview features.
    '''
    return call_az("az feature list", locals())


def show(name, namespace):
    return call_az("az feature show", locals())


def register(name, namespace):
    '''
    register a preview feature.
    '''
    return call_az("az feature register", locals())


def unregister(name, namespace):
    '''
    unregister a preview feature.
    '''
    return call_az("az feature unregister", locals())

