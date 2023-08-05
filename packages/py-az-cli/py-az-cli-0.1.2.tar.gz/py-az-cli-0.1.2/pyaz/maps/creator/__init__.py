from ... pyaz_utils import call_az

def list(name, resource_group):
    '''
    Get all Creator instances for an Azure Maps Account.
    '''
    return call_az("az maps creator list", locals())


def show(creator_name, name, resource_group):
    '''
    Get a Maps Creator resource.
    '''
    return call_az("az maps creator show", locals())


def create(creator_name, name, resource_group, storage_units, location=None, tags=None):
    '''
    Create a Maps Creator resource. Creator resource will manage Azure resources required to populate a custom set of mapping data. It requires an account to exist before it can be created.
    '''
    return call_az("az maps creator create", locals())


def update(creator_name, name, resource_group, storage_units=None, tags=None):
    '''
    Updates the Maps Creator resource. Only a subset of the parameters may be updated after creation, such as Tags.
    '''
    return call_az("az maps creator update", locals())


def delete(creator_name, name, resource_group, yes=None):
    '''
    Delete a Maps Creator resource.
    '''
    return call_az("az maps creator delete", locals())

