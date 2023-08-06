from ... pyaz_utils import _call_az

def list(hsm_name=None, resource_group=None, vault_name=None):
    '''
    List the private link resources supported for a Key Vault/HSM.
    '''
    return _call_az("az keyvault private-link-resource list", locals())

