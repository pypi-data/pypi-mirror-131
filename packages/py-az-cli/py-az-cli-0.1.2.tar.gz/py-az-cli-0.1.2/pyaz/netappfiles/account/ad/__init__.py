from .... pyaz_utils import call_az

def add(dns, domain, name, password, resource_group, smb_server_name, username, ad_name=None, add=None, administrators=None, aes_encryption=None, allow_local_ldap_users=None, backup_operators=None, force_string=None, kdc_ip=None, ldap_over_tls=None, ldap_signing=None, organizational_unit=None, remove=None, security_operators=None, server_root_ca_cert=None, set=None, tags=None):
    '''
    Add an active directory to the account.
    '''
    return call_az("az netappfiles account ad add", locals())


def list(name, resource_group):
    '''
    List the active directories of an account.
    '''
    return call_az("az netappfiles account ad list", locals())


def remove(active_directory, name, resource_group):
    '''
    Remove an active directory from the account.
    '''
    return call_az("az netappfiles account ad remove", locals())

