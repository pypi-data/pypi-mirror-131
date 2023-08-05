from ... pyaz_utils import call_az

def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Webchat Channel on a bot
    '''
    return call_az("az bot webchat show", locals())

