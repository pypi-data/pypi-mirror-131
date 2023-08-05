from ... pyaz_utils import call_az

def list(hsm_name=None, resource_group=None, vault_name=None):
    '''
    List the private link resources supported for a Key Vault/HSM.
    '''
    return call_az("az keyvault private-link-resource list", locals())

