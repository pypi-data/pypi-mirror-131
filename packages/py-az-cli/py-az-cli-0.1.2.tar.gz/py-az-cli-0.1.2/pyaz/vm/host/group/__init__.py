from .... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Get the details of a dedicated host group.
    '''
    return call_az("az vm host group show", locals())


def get_instance_view(name, resource_group):
    '''
    Get instance view of a dedicated host group.
    '''
    return call_az("az vm host group get-instance-view", locals())


def create(name, platform_fault_domain_count, resource_group, automatic_placement=None, location=None, tags=None, zone=None):
    '''
    Create a dedicated host group.
    '''
    return call_az("az vm host group create", locals())


def list(resource_group=None):
    '''
    List dedicated host groups.
    '''
    return call_az("az vm host group list", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Update a dedicated host group.
    '''
    return call_az("az vm host group update", locals())


def delete(name, resource_group, yes=None):
    return call_az("az vm host group delete", locals())

