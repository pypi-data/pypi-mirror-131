from ... pyaz_utils import call_az

def approve(description=None, hsm_name=None, id=None, name=None, no_wait=None, resource_group=None, vault_name=None):
    '''
    Approve a private endpoint connection request for a Key Vault/HSM.
    '''
    return call_az("az keyvault private-endpoint-connection approve", locals())


def reject(description=None, hsm_name=None, id=None, name=None, no_wait=None, resource_group=None, vault_name=None):
    '''
    Reject a private endpoint connection request for a Key Vault/HSM.
    '''
    return call_az("az keyvault private-endpoint-connection reject", locals())


def delete(hsm_name=None, id=None, name=None, no_wait=None, resource_group=None, vault_name=None):
    '''
    Delete the specified private endpoint connection associated with a Key Vault/HSM.
    '''
    return call_az("az keyvault private-endpoint-connection delete", locals())


def list(hsm_name, resource_group=None):
    '''
    List all private endpoint connections associated with a HSM.
    '''
    return call_az("az keyvault private-endpoint-connection list", locals())


def show(hsm_name=None, id=None, name=None, resource_group=None, vault_name=None):
    '''
    Show details of a private endpoint connection associated with a Key Vault/HSM.
    '''
    return call_az("az keyvault private-endpoint-connection show", locals())


def wait(created=None, custom=None, deleted=None, exists=None, hsm_name=None, id=None, interval=None, name=None, resource_group=None, timeout=None, updated=None, vault_name=None):
    '''
    Place the CLI in a waiting state until a condition of the private endpoint connection is met.
    '''
    return call_az("az keyvault private-endpoint-connection wait", locals())

