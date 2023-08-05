from .... pyaz_utils import call_az

def add(account_name, name, policy_option_name, resource_group, alt_rsa_token_keys=None, alt_symmetric_token_keys=None, alt_x509_token_keys=None, ask=None, audience=None, clear_key_configuration=None, fair_play_pfx=None, fair_play_pfx_password=None, fp_playback_duration_seconds=None, fp_storage_duration_seconds=None, issuer=None, open_id_connect_discovery_document=None, open_restriction=None, play_ready_template=None, rental_and_lease_key_type=None, rental_duration=None, token_claims=None, token_key=None, token_key_type=None, token_type=None, widevine_template=None):
    '''
    Add a new option to an existing content key policy.
    '''
    return call_az("az ams content-key-policy option add", locals())


def remove(account_name, name, policy_option_id, resource_group):
    '''
    Remove an option from an existing content key policy.
    '''
    return call_az("az ams content-key-policy option remove", locals())


def update(account_name, name, policy_option_id, resource_group, add_alt_token_key=None, add_alt_token_key_type=None, ask=None, audience=None, fair_play_pfx=None, fair_play_pfx_password=None, fp_playback_duration_seconds=None, fp_storage_duration_seconds=None, issuer=None, open_id_connect_discovery_document=None, play_ready_template=None, policy_option_name=None, rental_and_lease_key_type=None, rental_duration=None, token_claims=None, token_key=None, token_key_type=None, token_type=None, widevine_template=None):
    '''
    Update an option from an existing content key policy.
    '''
    return call_az("az ams content-key-policy option update", locals())

