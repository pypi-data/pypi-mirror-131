from ... pyaz_utils import call_az

def list(account_name, resource_group):
    '''
    List the ANF vaults for NetApp Account.
    '''
    return call_az("az netappfiles vault list", locals())

