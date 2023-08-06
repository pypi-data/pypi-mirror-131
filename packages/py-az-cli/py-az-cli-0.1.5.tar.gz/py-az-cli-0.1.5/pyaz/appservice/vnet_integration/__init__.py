from ... pyaz_utils import _call_az

def list(plan, resource_group):
    '''
    list the virtual network integrations used in an appservice plan
    '''
    return _call_az("az appservice vnet-integration list", locals())

