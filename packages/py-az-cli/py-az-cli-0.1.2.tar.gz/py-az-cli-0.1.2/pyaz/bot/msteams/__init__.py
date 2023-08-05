from ... pyaz_utils import call_az

def create(name, resource_group, add_disabled=None, calling_web_hook=None, enable_calling=None):
    '''
    Create the Microsoft Teams Channel on a bot.
    '''
    return call_az("az bot msteams create", locals())


def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Microsoft Teams Channel on a bot
    '''
    return call_az("az bot msteams show", locals())


def delete(name, resource_group):
    '''
    Delete the Microsoft Teams Channel on a bot
    '''
    return call_az("az bot msteams delete", locals())

