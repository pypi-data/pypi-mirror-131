from .... pyaz_utils import call_az

def show(account_name, resource_group=None):
    '''
    Show the properties of file service in storage account.
    '''
    return call_az("az storage account file-service-properties show", locals())


def update(account_name, add=None, auth_methods=None, channel_encryption=None, delete_retention_days=None, enable_delete_retention=None, enable_smb_multichannel=None, force_string=None, kerb_ticket_encryption=None, remove=None, resource_group=None, set=None, versions=None):
    '''
    Update the properties of file service in storage account.
    '''
    return call_az("az storage account file-service-properties update", locals())

