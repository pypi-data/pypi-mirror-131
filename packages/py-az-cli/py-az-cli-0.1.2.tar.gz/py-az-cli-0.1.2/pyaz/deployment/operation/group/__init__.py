from .... pyaz_utils import call_az

def list(name, resource_group):
    '''
    List deployment operations at resource group.
    '''
    return call_az("az deployment operation group list", locals())


def show(name, operation_ids, resource_group):
    '''
    Show a deployment operation at resource group.
    '''
    return call_az("az deployment operation group show", locals())

