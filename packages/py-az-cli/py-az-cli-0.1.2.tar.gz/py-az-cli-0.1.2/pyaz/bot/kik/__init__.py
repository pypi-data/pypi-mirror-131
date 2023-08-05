from ... pyaz_utils import call_az

def create(key, name, resource_group, user_name, add_disabled=None, is_validated=None):
    '''
    Create the Kik Channel on a bot.
    '''
    return call_az("az bot kik create", locals())


def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Kik Channel on a bot
    '''
    return call_az("az bot kik show", locals())


def delete(name, resource_group):
    '''
    Delete the Kik Channel on a bot
    '''
    return call_az("az bot kik delete", locals())

