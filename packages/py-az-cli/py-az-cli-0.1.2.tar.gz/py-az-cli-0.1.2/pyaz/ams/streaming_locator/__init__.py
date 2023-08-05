from ... pyaz_utils import call_az

def create(account_name, asset_name, name, resource_group, streaming_policy_name, alternative_media_id=None, content_key_policy_name=None, content_keys=None, end_time=None, filters=None, start_time=None, streaming_locator_id=None):
    '''
    Create a streaming locator.
    '''
    return call_az("az ams streaming-locator create", locals())


def list(account_name, resource_group, filter=None, orderby=None, top=None):
    '''
    List all the streaming locators within an Azure Media Services account.
    '''
    return call_az("az ams streaming-locator list", locals())


def show(account_name, name, resource_group):
    '''
    Show the details of a streaming locator.
    '''
    return call_az("az ams streaming-locator show", locals())


def delete(account_name, name, resource_group):
    return call_az("az ams streaming-locator delete", locals())


def get_paths(account_name, name, resource_group):
    '''
    List paths supported by a streaming locator.
    '''
    return call_az("az ams streaming-locator get-paths", locals())


def list_content_keys(account_name, name, resource_group):
    '''
    List content keys used by a streaming locator.
    '''
    return call_az("az ams streaming-locator list-content-keys", locals())

