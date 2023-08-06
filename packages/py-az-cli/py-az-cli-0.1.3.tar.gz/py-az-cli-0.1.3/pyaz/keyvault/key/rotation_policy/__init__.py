from .... pyaz_utils import _call_az

def show(hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Get the rotation policy of a Key Vault key.
    '''
    return _call_az("az keyvault key rotation-policy show", locals())


def update(value, hsm_name=None, id=None, name=None, vault_name=None):
    '''
    Update the rotation policy of a Key Vault key.
    '''
    return _call_az("az keyvault key rotation-policy update", locals())

