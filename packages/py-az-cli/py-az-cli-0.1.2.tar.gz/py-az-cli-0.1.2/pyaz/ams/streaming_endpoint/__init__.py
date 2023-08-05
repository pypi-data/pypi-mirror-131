from ... pyaz_utils import call_az
from . import akamai


def list(account_name, resource_group):
    '''
    List all the streaming endpoints within an Azure Media Services account.
    '''
    return call_az("az ams streaming-endpoint list", locals())


def start(account_name, name, resource_group, no_wait=None):
    '''
    Start a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint start", locals())


def stop(account_name, name, resource_group, no_wait=None):
    '''
    Stop a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint stop", locals())


def create(account_name, name, resource_group, scale_units, auto_start=None, availability_set_name=None, cdn_profile=None, cdn_provider=None, client_access_policy=None, cross_domain_policy=None, custom_host_names=None, description=None, ips=None, max_cache_age=None, no_wait=None, tags=None):
    '''
    Create a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint create", locals())


def scale(account_name, name, resource_group, scale_units):
    '''
    Set the scale of a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint scale", locals())


def update(account_name, name, resource_group, add=None, cdn_profile=None, cdn_provider=None, client_access_policy=None, cross_domain_policy=None, custom_host_names=None, description=None, disable_cdn=None, force_string=None, ips=None, max_cache_age=None, no_wait=None, remove=None, set=None, tags=None):
    '''
    Update the details of a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint update", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint show", locals())


def delete(account_name, name, resource_group):
    '''
    Delete a streaming endpoint.
    '''
    return call_az("az ams streaming-endpoint delete", locals())


def wait(account_name, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the streaming endpoint is met.
    '''
    return call_az("az ams streaming-endpoint wait", locals())

