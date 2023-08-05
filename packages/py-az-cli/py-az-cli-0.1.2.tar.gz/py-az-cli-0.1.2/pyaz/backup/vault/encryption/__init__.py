from .... pyaz_utils import call_az

def update(encryption_key_id, name, resource_group, infrastructure_encryption=None, mi_system_assigned=None, mi_user_assigned=None):
    '''
    Update encryption properties of a Recovery Services Vault.
    '''
    return call_az("az backup vault encryption update", locals())


def show(name, resource_group):
    '''
    Show details of encryption properties of a Recovery Services Vault.
    '''
    return call_az("az backup vault encryption show", locals())

