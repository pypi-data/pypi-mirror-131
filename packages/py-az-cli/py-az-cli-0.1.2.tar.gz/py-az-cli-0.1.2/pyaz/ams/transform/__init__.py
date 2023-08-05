from ... pyaz_utils import call_az
from . import output


def show(account_name, name, resource_group):
    '''
    Show the details of a transform.
    '''
    return call_az("az ams transform show", locals())


def list(account_name, resource_group, filter=None, orderby=None):
    '''
    List all the transforms of an Azure Media Services account.
    '''
    return call_az("az ams transform list", locals())


def delete(account_name, name, resource_group):
    '''
    Delete a transform.
    '''
    return call_az("az ams transform delete", locals())


def create(account_name, name, preset, resource_group, audio_analysis_mode=None, audio_language=None, description=None, insights_to_extract=None, on_error=None, relative_priority=None, resolution=None, video_analysis_mode=None):
    '''
    Create a transform.
    '''
    return call_az("az ams transform create", locals())


def update(account_name, name, resource_group, add=None, description=None, force_string=None, remove=None, set=None):
    '''
    Update the details of a transform.
    '''
    return call_az("az ams transform update", locals())

