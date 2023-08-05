from ... pyaz_utils import call_az

def create(account_name, name, resource_group, cbcs_clear_tracks=None, cbcs_default_key_label=None, cbcs_default_key_policy_name=None, cbcs_fair_play_allow_persistent_license=None, cbcs_fair_play_template=None, cbcs_key_to_track_mappings=None, cbcs_play_ready_attributes=None, cbcs_play_ready_template=None, cbcs_protocols=None, cbcs_widevine_template=None, cenc_clear_tracks=None, cenc_default_key_label=None, cenc_default_key_policy_name=None, cenc_disable_play_ready=None, cenc_disable_widevine=None, cenc_key_to_track_mappings=None, cenc_play_ready_attributes=None, cenc_play_ready_template=None, cenc_protocols=None, cenc_widevine_template=None, default_content_key_policy_name=None, envelope_clear_tracks=None, envelope_default_key_label=None, envelope_default_key_policy_name=None, envelope_key_to_track_mappings=None, envelope_protocols=None, envelope_template=None, no_encryption_protocols=None):
    '''
    Create a streaming policy.
    '''
    return call_az("az ams streaming-policy create", locals())


def list(account_name, resource_group, filter=None, orderby=None, top=None):
    '''
    List all the streaming policies within an Azure Media Services account.
    '''
    return call_az("az ams streaming-policy list", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a streaming policy.
    '''
    return call_az("az ams streaming-policy show", locals())


def delete(account_name, name, resource_group):
    return call_az("az ams streaming-policy delete", locals())

