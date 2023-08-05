from .. pyaz_utils import call_az
from . import param_persist


def set(local=None):
    '''
    Set a configuration.
    '''
    return call_az("az config set", locals())


def get(local=None):
    '''
    Get a configuration.
    '''
    return call_az("az config get", locals())


def unset(local=None):
    '''
    Unset a configuration.
    '''
    return call_az("az config unset", locals())

