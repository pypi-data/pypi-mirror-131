from .... pyaz_utils import call_az

def add(account_name, name, preset, resource_group, audio_analysis_mode=None, audio_language=None, insights_to_extract=None, on_error=None, relative_priority=None, resolution=None, video_analysis_mode=None):
    '''
    Add an output to an existing transform.
    '''
    return call_az("az ams transform output add", locals())


def remove(account_name, name, output_index, resource_group):
    '''
    Remove an output from an existing transform.
    '''
    return call_az("az ams transform output remove", locals())

