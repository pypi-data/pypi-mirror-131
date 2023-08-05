from .... pyaz_utils import call_az

def list(account_endpoint=None, account_key=None, account_name=None, filter=None):
    '''
    Lists all Virtual Machine Images supported by the Azure Batch service.
    '''
    return call_az("az batch pool supported-images list", locals())

