from ... pyaz_utils import call_az

def create(account_name, archive_window_length, asset_name, live_event_name, name, resource_group, description=None, fragments_per_ts_segment=None, manifest_name=None, output_snap_time=None):
    '''
    Create a live output.
    '''
    return call_az("az ams live-output create", locals())


def show(account_name, live_event_name, name, resource_group):
    '''
    Show the details of a live output.
    '''
    return call_az("az ams live-output show", locals())


def list(account_name, live_event_name, resource_group):
    '''
    List all the live outputs in a live event.
    '''
    return call_az("az ams live-output list", locals())


def delete(account_name, live_event_name, name, resource_group):
    '''
    Delete a live output.
    '''
    return call_az("az ams live-output delete", locals())

