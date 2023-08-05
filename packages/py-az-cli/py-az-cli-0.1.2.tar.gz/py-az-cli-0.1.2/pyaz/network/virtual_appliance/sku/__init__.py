from .... pyaz_utils import call_az

def show(name):
    '''
    Show the detail of an Azure network virtual appliance sku.
    '''
    return call_az("az network virtual-appliance sku show", locals())


def list():
    '''
    List all Azure network virtual appliance sku.
    '''
    return call_az("az network virtual-appliance sku list", locals())

