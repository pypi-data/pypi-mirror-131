from ... pyaz_utils import call_az

def show(name, resource_group, vault_name, backup_management_type=None, use_secondary_region=None):
    '''
    Show details of a container registered to a Recovery services vault.
    '''
    return call_az("az backup container show", locals())


def list(backup_management_type, resource_group, vault_name, use_secondary_region=None):
    '''
    List containers registered to a Recovery services vault.
    '''
    return call_az("az backup container list", locals())


def unregister(container_name, resource_group, vault_name, backup_management_type=None, yes=None):
    '''
    Unregister a Backup Container to make the underlying 'resource' be protected by another vault.
    '''
    return call_az("az backup container unregister", locals())


def re_register(container_name, resource_group, vault_name, workload_type, backup_management_type=None, yes=None):
    '''
    Reset the registration details for a given container.
    '''
    return call_az("az backup container re-register", locals())


def register(resource_group, resource_id, vault_name, workload_type, backup_management_type=None):
    '''
    Register a Resource to the given Recovery Services Vault.
    '''
    return call_az("az backup container register", locals())

