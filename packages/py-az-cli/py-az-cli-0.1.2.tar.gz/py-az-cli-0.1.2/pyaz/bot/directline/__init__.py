from ... pyaz_utils import call_az

def create(name, resource_group, add_disabled=None, disablev1=None, disablev3=None, enable_enhanced_auth=None, trusted_origins=None):
    '''
    Create the DirectLine Channel on a bot with only v3 protocol enabled.
    '''
    return call_az("az bot directline create", locals())


def update(name, resource_group, add_disabled=None, disablev1=None, disablev3=None, enable_enhanced_auth=None, trusted_origins=None):
    '''
    Update the DirectLine Channel on a bot with only v3 protocol enabled.
    '''
    return call_az("az bot directline update", locals())


def show(name, resource_group, with_secrets=None):
    '''
    Get details of the Directline Channel on a bot
    '''
    return call_az("az bot directline show", locals())


def delete(name, resource_group):
    '''
    Delete the Directline Channel on a bot
    '''
    return call_az("az bot directline delete", locals())

