from ... pyaz_utils import call_az

def start(storage_container_SAS_token, blob_container_name=None, hsm_name=None, id=None, storage_account_name=None, storage_resource_uri=None):
    '''
    Begin a full backup of the HSM.
    '''
    return call_az("az keyvault backup start", locals())

