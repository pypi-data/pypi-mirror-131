from ... pyaz_utils import call_az
from . import filter


def set(auth_mode=None, connection_string=None, description=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Set a feature flag.
    '''
    return call_az("az appconfig feature set", locals())


def delete(auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Delete feature flag.
    '''
    return call_az("az appconfig feature delete", locals())


def show(auth_mode=None, connection_string=None, endpoint=None, feature=None, fields=None, key=None, label=None, name=None):
    '''
    Show all attributes of a feature flag.
    '''
    return call_az("az appconfig feature show", locals())


def list(all=None, auth_mode=None, connection_string=None, endpoint=None, feature=None, fields=None, key=None, label=None, name=None, top=None):
    '''
    List feature flags.
    '''
    return call_az("az appconfig feature list", locals())


def lock(auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Lock a feature flag to prohibit write operations.
    '''
    return call_az("az appconfig feature lock", locals())


def unlock(auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Unlock a feature to gain write operations.
    '''
    return call_az("az appconfig feature unlock", locals())


def enable(auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Enable a feature flag to turn it ON for use.
    '''
    return call_az("az appconfig feature enable", locals())


def disable(auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, yes=None):
    '''
    Disable a feature flag to turn it OFF for use.
    '''
    return call_az("az appconfig feature disable", locals())

