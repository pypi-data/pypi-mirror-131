from .... pyaz_utils import call_az

def show(account_name, resource_group):
    '''
    Show the details of encryption settings for an Azure Media Services account.
    '''
    return call_az("az ams account encryption show", locals())


def set(account_name, key_type, resource_group, current_key_id=None, key_identifier=None):
    '''
    Set the encryption settings for an Azure Media Services account.
    '''
    return call_az("az ams account encryption set", locals())

