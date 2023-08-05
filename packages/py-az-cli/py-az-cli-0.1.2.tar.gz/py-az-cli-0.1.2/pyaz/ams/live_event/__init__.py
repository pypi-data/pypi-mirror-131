from ... pyaz_utils import call_az

def create(account_name, ips, name, resource_group, streaming_protocol, access_token=None, alternative_media_id=None, auto_start=None, client_access_policy=None, cross_domain_policy=None, description=None, encoding_type=None, hostname_prefix=None, key_frame_interval=None, key_frame_interval_duration=None, no_wait=None, preset_name=None, preview_ips=None, preview_locator=None, stream_options=None, streaming_policy_name=None, stretch_mode=None, tags=None, transcription_lang=None, use_static_hostname=None):
    '''
    Create a live event.
    '''
    return call_az("az ams live-event create", locals())


def start(account_name, name, resource_group, no_wait=None):
    '''
    Start a live event.
    '''
    return call_az("az ams live-event start", locals())


def standby(account_name, name, resource_group, no_wait=None):
    '''
    Allocate a live event to be started later.
    '''
    return call_az("az ams live-event standby", locals())


def stop(account_name, name, resource_group, no_wait=None, remove_outputs_on_stop=None):
    '''
    Stop a live event.
    '''
    return call_az("az ams live-event stop", locals())


def reset(account_name, name, resource_group, no_wait=None):
    '''
    Reset a live event.
    '''
    return call_az("az ams live-event reset", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a live event.
    '''
    return call_az("az ams live-event show", locals())


def delete(account_name, name, resource_group):
    '''
    Delete a live event.
    '''
    return call_az("az ams live-event delete", locals())


def list(account_name, resource_group):
    '''
    List all the live events of an Azure Media Services account.
    '''
    return call_az("az ams live-event list", locals())


def update(account_name, name, resource_group, add=None, client_access_policy=None, cross_domain_policy=None, description=None, force_string=None, ips=None, key_frame_interval_duration=None, preview_ips=None, remove=None, set=None, tags=None):
    '''
    Update the details of a live event.
    '''
    return call_az("az ams live-event update", locals())


def wait(account_name, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the live event is met.
    '''
    return call_az("az ams live-event wait", locals())

