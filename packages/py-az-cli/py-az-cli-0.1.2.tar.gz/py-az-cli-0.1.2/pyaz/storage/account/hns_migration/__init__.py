from .... pyaz_utils import call_az

def start(name, type, no_wait=None, resource_group=None):
    '''
    Validate/Begin migrating a storage account to enable hierarchical namespace.
    '''
    return call_az("az storage account hns-migration start", locals())


def stop(name, no_wait=None, resource_group=None):
    '''
    Stop the enabling hierarchical namespace migration of a storage account.
    '''
    return call_az("az storage account hns-migration stop", locals())

