from .... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Show the details of media reserved units for an Azure Media Services account. This doesn't work with accounts created with 2020-05-01 version of the Media Services API or later. Accounts created this way no longer need to set media reserved units as the system will automaticaly scale up and down based on load.
    '''
    return call_az("az ams account mru show", locals())


def set(name, resource_group, count=None, type=None):
    '''
    Set the type and number of media reserved units for an Azure Media Services account. This doesn't work with accounts created with 2020-05-01 version of the Media Services API or later. Accounts created this way no longer need to set media reserved units as the system will automaticaly scale up and down based on load.
    '''
    return call_az("az ams account mru set", locals())

