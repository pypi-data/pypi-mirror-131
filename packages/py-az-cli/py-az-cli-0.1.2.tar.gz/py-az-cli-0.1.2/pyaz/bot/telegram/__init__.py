from ... pyaz_utils import call_az

def create(access_token, name, resource_group, add_disabled=None, is_validated=None):
    '''
    Create the Telegram Channel on a bot.
    '''
    return call_az("az bot telegram create", locals())


def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Telegram Channel on a bot
    '''
    return call_az("az bot telegram show", locals())


def delete(name, resource_group):
    '''
    Delete the Telegram Channel on a bot
    '''
    return call_az("az bot telegram delete", locals())

