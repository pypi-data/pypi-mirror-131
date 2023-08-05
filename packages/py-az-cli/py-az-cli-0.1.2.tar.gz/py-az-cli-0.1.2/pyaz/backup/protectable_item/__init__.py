from ... pyaz_utils import call_az

def show(name, protectable_item_type, resource_group, server_name, vault_name, workload_type):
    '''
    Retrieve the specified protectable item within the given container.
    '''
    return call_az("az backup protectable-item show", locals())


def list(resource_group, vault_name, workload_type, backup_management_type=None, container_name=None, protectable_item_type=None, server_name=None):
    '''
    Retrieve all protectable items within a certain container or across all registered containers.
    '''
    return call_az("az backup protectable-item list", locals())


def initialize(container_name, resource_group, vault_name, workload_type):
    '''
    Trigger the discovery of any unprotected items of the given workload type in the given container.
    '''
    return call_az("az backup protectable-item initialize", locals())

