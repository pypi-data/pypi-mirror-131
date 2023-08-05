from ... pyaz_utils import call_az
from . import option


def create(account_name, name, policy_option_name, resource_group, alt_rsa_token_keys=None, alt_symmetric_token_keys=None, alt_x509_token_keys=None, ask=None, audience=None, clear_key_configuration=None, description=None, fair_play_pfx=None, fair_play_pfx_password=None, fp_playback_duration_seconds=None, fp_storage_duration_seconds=None, issuer=None, open_id_connect_discovery_document=None, open_restriction=None, play_ready_template=None, rental_and_lease_key_type=None, rental_duration=None, token_claims=None, token_key=None, token_key_type=None, token_type=None, widevine_template=None):
    '''
    Create a new content key policy.
    '''
    return call_az("az ams content-key-policy create", locals())


def show(account_name, name, resource_group, with_secrets=None):
    '''
    Show an existing content key policy.
    '''
    return call_az("az ams content-key-policy show", locals())


def delete(account_name, name, resource_group):
    '''
    Delete a content key policy.
    '''
    return call_az("az ams content-key-policy delete", locals())


def list(account_name, resource_group, filter=None, orderby=None, top=None):
    '''
    List all the content key policies within an Azure Media Services account.
    '''
    return call_az("az ams content-key-policy list", locals())


def update(account_name, name, resource_group, add=None, description=None, force_string=None, remove=None, set=None):
    '''
    Update an existing content key policy.
    '''
    return call_az("az ams content-key-policy update", locals())

