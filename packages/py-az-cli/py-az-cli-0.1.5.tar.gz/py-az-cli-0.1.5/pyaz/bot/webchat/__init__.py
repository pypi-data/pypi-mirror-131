from ... pyaz_utils import _call_az

def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Webchat Channel on a bot
    '''
    return _call_az("az bot webchat show", locals())

