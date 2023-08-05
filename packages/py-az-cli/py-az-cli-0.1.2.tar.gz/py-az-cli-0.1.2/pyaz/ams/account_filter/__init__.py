from ... pyaz_utils import call_az

def create(account_name, name, resource_group, bitrate=None, end_timestamp=None, first_quality=None, force_end_timestamp=None, live_backoff_duration=None, presentation_window_duration=None, start_timestamp=None, timescale=None, tracks=None):
    '''
    Create an account filter.
    '''
    return call_az("az ams account-filter create", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of an account filter.
    '''
    return call_az("az ams account-filter show", locals())


def list(account_name, resource_group):
    '''
    List all the account filters of an Azure Media Services account.
    '''
    return call_az("az ams account-filter list", locals())


def delete(account_name, name, resource_group):
    '''
    Delete an account filter.
    '''
    return call_az("az ams account-filter delete", locals())


def update(account_name, name, resource_group, add=None, bitrate=None, end_timestamp=None, first_quality=None, force_end_timestamp=None, force_string=None, live_backoff_duration=None, presentation_window_duration=None, remove=None, set=None, start_timestamp=None, timescale=None, tracks=None):
    '''
    Update the details of an account filter.
    '''
    return call_az("az ams account-filter update", locals())

