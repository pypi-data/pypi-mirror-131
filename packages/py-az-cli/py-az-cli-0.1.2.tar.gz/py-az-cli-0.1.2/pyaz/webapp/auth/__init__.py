from ... pyaz_utils import call_az

def show(name, resource_group, slot=None):
    '''
    Show the authentification settings for the webapp.
    '''
    return call_az("az webapp auth show", locals())


def update(name, resource_group, aad_allowed_token_audiences=None, aad_client_id=None, aad_client_secret=None, aad_client_secret_certificate_thumbprint=None, aad_token_issuer_url=None, action=None, allowed_external_redirect_urls=None, enabled=None, facebook_app_id=None, facebook_app_secret=None, facebook_oauth_scopes=None, google_client_id=None, google_client_secret=None, google_oauth_scopes=None, microsoft_account_client_id=None, microsoft_account_client_secret=None, microsoft_account_oauth_scopes=None, runtime_version=None, slot=None, token_refresh_extension_hours=None, token_store=None, twitter_consumer_key=None, twitter_consumer_secret=None):
    '''
    Update the authentication settings for the webapp.
    '''
    return call_az("az webapp auth update", locals())

