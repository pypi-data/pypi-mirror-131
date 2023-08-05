from ... pyaz_utils import call_az

def start(backup_folder, storage_container_SAS_token, blob_container_name=None, hsm_name=None, id=None, storage_account_name=None, storage_resource_uri=None):
    '''
    Restore a full backup of a HSM.
    '''
    return call_az("az keyvault restore start", locals())

