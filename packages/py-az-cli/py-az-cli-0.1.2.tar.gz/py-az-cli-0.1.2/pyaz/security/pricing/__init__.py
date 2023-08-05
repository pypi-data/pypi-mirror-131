from ... pyaz_utils import call_az

def list():
    '''
    Shows the Azure Defender plans for the subscription.
    '''
    return call_az("az security pricing list", locals())


def show(name):
    '''
    Shows the Azure Defender plan for the subscription
    '''
    return call_az("az security pricing show", locals())


def create(name, tier):
    '''
    Updates the Azure defender plan for the subscription.
    '''
    return call_az("az security pricing create", locals())

