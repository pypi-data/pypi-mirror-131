from .. pyaz_utils import _call_az
from . import lock, management_group


def list(all=None, refresh=None):
    '''
    Get a list of subscriptions for the logged in account. By default, only 'Enabled' subscriptions from the current cloud is shown.
    '''
    return _call_az("az account list", locals())


def set(subscription):
    '''
    Set a subscription to be the current active subscription.
    '''
    return _call_az("az account set", locals())


def show(sdk_auth=None, subscription=None):
    '''
    Get the details of a subscription.
    '''
    return _call_az("az account show", locals())


def clear():
    '''
    Clear all subscriptions from the CLI's local cache.
    '''
    return _call_az("az account clear", locals())


def list_locations():
    '''
    List supported regions for the current subscription.
    '''
    return _call_az("az account list-locations", locals())


def get_access_token(resource=None, resource_type=None, scope=None, subscription=None, tenant=None):
    '''
    Get a token for utilities to access Azure.
    '''
    return _call_az("az account get-access-token", locals())

