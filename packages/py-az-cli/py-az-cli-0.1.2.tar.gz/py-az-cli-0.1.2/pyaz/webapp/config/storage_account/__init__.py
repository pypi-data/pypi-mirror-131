from .... pyaz_utils import call_az

def list(name, resource_group, slot=None):
    '''
    Get a web app's Azure storage account configurations. (Linux Web Apps and Windows Containers Web Apps Only)
    '''
    return call_az("az webapp config storage-account list", locals())


def add(access_key, account_name, custom_id, name, resource_group, share_name, storage_type, mount_path=None, slot=None, slot_setting=None):
    '''
    Add an Azure storage account configuration to a web app. (Linux Web Apps and Windows Containers Web Apps Only)
    '''
    return call_az("az webapp config storage-account add", locals())


def update(custom_id, name, resource_group, access_key=None, account_name=None, mount_path=None, share_name=None, slot=None, slot_setting=None, storage_type=None):
    '''
    Update an existing Azure storage account configuration on a web app. (Linux Web Apps and Windows Containers Web Apps Only)
    '''
    return call_az("az webapp config storage-account update", locals())


def delete(custom_id, name, resource_group, slot=None):
    '''
    Delete a web app's Azure storage account configuration. (Linux Web Apps and Windows Containers Web Apps Only)
    '''
    return call_az("az webapp config storage-account delete", locals())

