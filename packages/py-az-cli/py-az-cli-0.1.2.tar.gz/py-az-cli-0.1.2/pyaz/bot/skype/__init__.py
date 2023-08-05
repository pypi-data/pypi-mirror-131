from ... pyaz_utils import call_az

def create(name, resource_group, add_disabled=None, calling_web_hook=None, enable_calling=None, enable_groups=None, enable_media_cards=None, enable_messaging=None, enable_screen_sharing=None, enable_video=None, groups_mode=None):
    '''
    Create the Skype Channel on a bot.
    '''
    return call_az("az bot skype create", locals())


def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Skype Channel on a bot
    '''
    return call_az("az bot skype show", locals())


def delete(name, resource_group):
    '''
    Delete the Skype Channel on a bot
    '''
    return call_az("az bot skype delete", locals())

