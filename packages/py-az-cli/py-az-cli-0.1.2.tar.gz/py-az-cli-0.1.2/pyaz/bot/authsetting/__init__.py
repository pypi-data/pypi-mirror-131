from ... pyaz_utils import call_az

def list(name, resource_group):
    '''
    Show all OAuth connection settings on a bot.
    '''
    return call_az("az bot authsetting list", locals())


def show(name, resource_group, setting_name):
    '''
    Show details of an OAuth connection setting on a bot.
    '''
    return call_az("az bot authsetting show", locals())


def delete(name, resource_group, setting_name):
    '''
    Delete an OAuth connection setting on a bot.
    '''
    return call_az("az bot authsetting delete", locals())


def create(client_id, client_secret, name, provider_scope_string, resource_group, service, setting_name, parameters=None):
    '''
    Create an OAuth connection setting on a bot.
    '''
    return call_az("az bot authsetting create", locals())


def list_providers(provider_name=None):
    '''
    List details for all service providers available for creating OAuth connection settings.
    '''
    return call_az("az bot authsetting list-providers", locals())

