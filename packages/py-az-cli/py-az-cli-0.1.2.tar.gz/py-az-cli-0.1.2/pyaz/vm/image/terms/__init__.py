from .... pyaz_utils import call_az

def accept(offer=None, plan=None, publisher=None, urn=None):
    '''
    Accept Azure Marketplace image terms so that the image can be used to create VMs.
    '''
    return call_az("az vm image terms accept", locals())


def cancel(offer=None, plan=None, publisher=None, urn=None):
    '''
    Cancel Azure Marketplace image terms.
    '''
    return call_az("az vm image terms cancel", locals())


def show(offer=None, plan=None, publisher=None, urn=None):
    '''
    Get the details of Azure Marketplace image terms.
    '''
    return call_az("az vm image terms show", locals())

