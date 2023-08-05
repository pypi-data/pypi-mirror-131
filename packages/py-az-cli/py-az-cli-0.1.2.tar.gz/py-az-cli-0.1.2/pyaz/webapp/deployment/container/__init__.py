from .... pyaz_utils import call_az

def config(enable_cd, name, resource_group, slot=None):
    '''
    Configure continuous deployment via containers.
    '''
    return call_az("az webapp deployment container config", locals())


def show_cd_url(name, resource_group, slot=None):
    '''
    Get the URL which can be used to configure webhooks for continuous deployment.
    '''
    return call_az("az webapp deployment container show-cd-url", locals())

