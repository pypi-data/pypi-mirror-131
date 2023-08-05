from ... pyaz_utils import call_az

def list():
    '''
    List the auto provisioning settings.
    '''
    return call_az("az security auto-provisioning-setting list", locals())


def show(name):
    '''
    Shows an auto provisioning setting.
    '''
    return call_az("az security auto-provisioning-setting show", locals())


def update(auto_provision, name):
    '''
    Updates your automatic provisioning settings on the subscription.
    '''
    return call_az("az security auto-provisioning-setting update", locals())

