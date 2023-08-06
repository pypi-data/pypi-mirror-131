from .... pyaz_utils import _call_az

def config(enable_cd, name, resource_group, slot=None):
    '''
    Configure continuous deployment via containers.
    '''
    return _call_az("az functionapp deployment container config", locals())


def show_cd_url(name, resource_group, slot=None):
    '''
    Get the URL which can be used to configure webhooks for continuous deployment.
    '''
    return _call_az("az functionapp deployment container show-cd-url", locals())

