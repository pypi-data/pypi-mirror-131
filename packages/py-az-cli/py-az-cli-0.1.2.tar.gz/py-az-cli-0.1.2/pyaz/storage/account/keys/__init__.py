from .... pyaz_utils import call_az

def renew(account_name, key, key_type=None, resource_group=None):
    '''
    Regenerate one of the access keys or Kerberos keys (if active directory enabled) for a storage account.
    '''
    return call_az("az storage account keys renew", locals())


def list(account_name, expand_key_type=None, resource_group=None):
    '''
    List the access keys or Kerberos keys (if active directory enabled) for a storage account.
    '''
    return call_az("az storage account keys list", locals())

